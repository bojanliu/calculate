#coding:utf-8
#file_name:calculate.py
"""此脚本用于根据一些条件计算某个数值"""
#time:20120411

import csv
import os
import time

def read_data():
    file_path=raw_input(u'请输入待处理文件：')
    f=open(file_path,'rb')
    data=f.read().split('\r\n')
    f.close()
    data=[item.split('\t') for item in data]
    return data

def parse_data(data):
    #最终加工好的数据形式为：{a:[[],[],[]],b:[[],[],[]],...}
    #该字典中每个value为list，该list里3个元素，均为不定长的list。
    data_dic={}
    list_1=[]
    list_2=[]
    list_3=[]
    list_1.append(data[0][1])
    list_2.append(data[0][2])
    list_3.append(data[0][3])

    #下面循环，前一项与后一项对比：首列相同则其余列数据写入相应list，
    for i in range(len(data)-1):
        #不同则创建新list
        if data[i][0]!=data[i+1][0]:
            list_1=[]
            list_2=[]
            list_3=[]
            
        list_1.append(data[i+1][1])
        list_2.append(data[i+1][2])
        list_3.append(data[i+1][3])
        
        data_dic[data[i+1][0]]=[list_1,#拆分后的关键词
                                list_2,#标题密度数值
                                list_3,#正文密度数值
                                ]
        i+=1

    return data_dic


def calculate(data_dic):
    for k,v in data_dic.items():
        for i in range(1,3):
            #为0才需要处理
            if v[i][0]=='0.00%':
                #计算是零的个数
                zero_count=v[i].count('0.00%')
                #此list中非零个数，当做分母
                denominator=len(v[i])-zero_count
                if denominator:
                    #去掉%号，将字符变为float
                    num_list=[float(item[:-1]) for item in v[i]]
                    result_num=sum(num_list)/denominator
                    v[i][0]=str(result_num)+'%'
        
    return data_dic
    
def create_csv(data_dic):
    f=open(os.path.join(os.getcwd(),'\\result_'+time.strftime('%M%S')+'.csv'),'wb')
    writer=csv.writer(f)
    for k,v in data_dic.items():
        for i in range(len(v[0])):
            writer.writerow([k,v[0][i],v[1][i],v[2][i]])

    f.close()

if __name__=='__main__':
    data=read_data()
    data_dic=parse_data(data)
    data_dic=calculate(data_dic)
    create_csv(data_dic)
    print 'ok!'
