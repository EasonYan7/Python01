# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 22:10:46 2022

@author: seyan
"""

import pandas as pd
import numpy as np
import datetime


# 数据处理
file1 = pd.read_csv(r'C:\work\产品\两融测算\两融测算\代码文件\全量等级.csv')
file1['create_time']=pd.to_datetime(file1['create_time'])
file2 = pd.read_excel(r'C:\work\产品\两融测算\两融测算\代码文件\两融4-10月目标变量.xlsx')
file2 = file2.loc[file2['Date']>=np.datetime64(datetime.datetime(2022,4,8))]
file1.rename({'st_code':'Stkcd','create_time':'Date'},axis=1,inplace=True)
file2.drop('Unnamed: 0', axis = 1, inplace=True)
# 对指标进行处理
file_all = pd.merge(file2,file1, on=['Stkcd','Date'])
#file_all=file_all.drop(file_all.loc[file_all['target']<0].index) 
file_all.loc[file_all['target']==0.1 ,'target']=0
file_all.loc[file_all['target']==0.8 ,'target']=1
file_all.sort_values(by=['Date','target'],ascending=True,inplace=True)
# 符合三种条件其一的list
file3 = pd.read_excel(r'C:\work\产品\两融测算\两融测算\代码文件\list.xlsx')
file_all = pd.merge(file3,file_all,how='left',on='Stkcd')
file_all.drop(['st_short_name'],axis=1,inplace=True)
# 去除含ST股票
file_all = file_all.drop(file_all.loc[file_all['Name'].str.contains('ST')].index)

tail_50 = {}
new_50 = {}
cal = pd.DataFrame(columns=['Date','cap_rate','acu_rate','cap_num'])
time_list = list(file_all['Date'].unique())
out_file = pd.DataFrame()



for time in time_list[:-1]:
    # 找出单日所有股票 对分数进行排序，选取#个坏样本
    time = pd.to_datetime(time,format="%Y-%m-%d")
    mod_list = file_all.loc[(file_all['Date']==time)]
    time = time.to_datetime64()
    mod_list.sort_values(by='平滑前得分',ascending=False,inplace=True)
    mod_list2 = file_all.loc[file_all['Date']==time]
    tail_50[time] = mod_list.tail(10)  #condition 1 每天多少高危主体
    # 加入窗口期，先将时间转换为可加减的格式，并筛选
    time = pd.to_datetime(time,format="%Y-%m-%d")
    sel_list = file_all[file_all['Date']< time + datetime.timedelta(days=90)]  #condition 2 天数
    sel_list = sel_list[sel_list['Date']>=time]
    # 时间转换完成，转回
    time = time.to_datetime64()
    # 对观察期内，发生改变的，进行分数迁移
    sub_50 = pd.merge(tail_50[time],sel_list.loc[sel_list['target']==1],how='left',on='Stkcd')
    sub_50.sort_values(by='Date_x',ascending=True,inplace=True)
    for st_index in range(len(sub_50)):
        lines = sub_50.iloc[st_index]
        if lines['target_y']!='nan':
           lines['target_x']=lines['target_y']
        sub_50.iloc[st_index]=lines
    sub_50.drop_duplicates(subset=['Stkcd'],inplace=True)
    sub_50.rename(columns = {'target_x':'target'},inplace=True)
    new_50[time] = sub_50
    # 单条件下的坏样本清单
    output_name = str(time)
    output_name = output_name[:10]
    out_file = pd.concat([out_file,sub_50.loc[sub_50['target']==1]])
    out_file.sort_values(by='Date_x',ascending=True,inplace=True)
    # 此处略繁杂，其实file_mini就是sub_50，不想改了
    # 对捕获率、准确率进行计算并汇总
    file_mini = new_50[time]
    acu_rate = len(file_mini.loc[file_mini['target']==1])/10  #condition 3 每天多少坏样本
    cap_rate = len(file_mini.loc[file_mini['target']==1])/20
    cap_num = len(file_mini.loc[file_mini['target']==1])
    cal_mini = pd.DataFrame({time:{'Date':time,'cap_rate':cap_rate,'acu_rate':acu_rate,'cap_num':cap_num}}).transpose()
    cal = pd.concat([cal,cal_mini],ignore_index=True)

#导出文件
cal.to_excel(r'C:\work\产品\两融测算\两融测算\cal_10_15Day.xlsx')
out_file.to_excel(r'C:\work\产品\两融测算\两融测算\target_list_10_60D.xlsx')
