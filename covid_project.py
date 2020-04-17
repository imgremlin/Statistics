import numpy as np
import pandas as pd
import re

ksi = [0.1,0.2,0.3,0.5,0.6,0.8,1]
eta = [i/14 for i in range(1,15)]

N = 4
p = 0.2
d = 0.03
exp_n = 10

df_res_liv = pd.DataFrame(np.zeros((90, exp_n)),
                columns=['exp_{}'.format(i) for i in range(1, exp_n + 1)])

#print(df_res_liv.head())
#for exp in range(exp_n)
df_iter = pd.DataFrame(np.zeros((90, N)),
                columns=['N_{}'.format(i) for i in range(1, N + 1)])

for i in range(1, N):
    df_iter.iloc[0,i] = 'liv'
   
df_iter.iloc[0,0] = 'ksi_0'
    
def regexp(name):
    num = re.findall(r"\d+", name)
    title = re.findall(r"[a-z]+", name)
    if len(num)==0:
        num = 'NONE'
        return title[0], num
    else:
        return title[0], num[0]
    
  
for day in range(89):  

    sick_count = 0  
    liv_index = []
    ksi_index = []
    eta_index = []
    dead_index = []
    
    for i in range(0, N):
    
        if regexp(df_iter.iloc[day,i])[0] == 'eta':
            sick_count += 1
            eta_index.append(i) 
        if regexp(df_iter.iloc[day,i])[0] == 'liv':
            liv_index.append(i)    
        if regexp(df_iter.iloc[day,i])[0] == 'ksi':
            ksi_index.append(i)
        if regexp(df_iter.iloc[day,i])[0] == 'dead':
            dead_index.append(i)
    #'''
        
    p_iter = 1 - ((1-p)**sick_count)
    
    for i in liv_index:
        if np.random.binomial(1, p_iter) == 1:
            df_iter.iloc[day+1,i] = 'ksi_0'
        else:
            df_iter.iloc[day+1,i] = 'liv'
    
    for i in ksi_index:
        if np.random.binomial(1, ksi[int(regexp(df_iter.iloc[day,i])[1])]) == 1:
            df_iter.iloc[day+1,i] = 'eta_0'
        else:
            next_num=int(regexp(df_iter.iloc[day,i])[1])+1
            df_iter.iloc[day+1,i] = 'ksi_{}'.format(next_num)
    
    for i in eta_index:
        if np.random.binomial(1, d) == 1:
            df_iter.iloc[day+1,i] = 'dead'
        else:
            if np.random.binomial(1, eta[int(regexp(df_iter.iloc[day,i])[1])]) == 1:
                df_iter.iloc[day+1,i] = 'liv'
            else:
                next_num=int(regexp(df_iter.iloc[day,i])[1])+1
                df_iter.iloc[day+1,i] = 'eta_{}'.format(next_num)
                
    for i in dead_index:
        df_iter.iloc[day+1,i] = 'dead'
print(df_iter)
