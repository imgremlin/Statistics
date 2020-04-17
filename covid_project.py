import numpy as np
import pandas as pd
import re
import seaborn as sns
from matplotlib import pyplot as plt

latent_rate = [0.1,0.2,0.3,0.5,0.6,0.8,0.9]
active_rate = [i/14 for i in range(1,15)]

n_people = 10
morbidity = 0.2
death_rate = 0.03
n_exp = 100
n_days = 90
n_infected = 1

df_res_alive = pd.DataFrame(np.zeros((n_days, n_exp)),
                columns=['exp_{}'.format(i) for i in range(1, n_exp + 1)])

df_res_dead = pd.DataFrame(np.zeros((n_days, n_exp)),
                columns=['exp_{}'.format(i) for i in range(1, n_exp + 1)])

df_res_active = pd.DataFrame(np.zeros((n_days, n_exp)),
                columns=['exp_{}'.format(i) for i in range(1, n_exp + 1)])

df_res_latent = pd.DataFrame(np.zeros((n_days, n_exp)),
                columns=['exp_{}'.format(i) for i in range(1, n_exp + 1)])

for exp in range(n_exp):
    df_iter = pd.DataFrame(np.zeros((n_days, n_people)),columns=['N_{}'.format(i) for i in range(1, n_people + 1)])
    
    for i in range(n_infected):
        df_iter.iloc[0,i] = 'latent_0'
    
    for i in range(n_infected, n_people):
        df_iter.iloc[0,i] = 'alive'
       
    def regexp(name):
        num = re.findall(r"\d+", name)
        title = re.findall(r"[a-z]+", name)
        if len(num)==0:
            num = 'NONE'
            return title[0], num
        else:
            return title[0], num[0]
        
      
    for day in range(n_days-1):  
    
        alive_index = []
        latent_index = []
        active_index = []
        dead_index = []
        
        for i in range(0, n_people):
        
            if regexp(df_iter.iloc[day,i])[0] == 'active':
                active_index.append(i) 
            if regexp(df_iter.iloc[day,i])[0] == 'alive':
                alive_index.append(i)    
            if regexp(df_iter.iloc[day,i])[0] == 'latent':
                latent_index.append(i)
            if regexp(df_iter.iloc[day,i])[0] == 'dead':
                dead_index.append(i)
                
        df_res_alive.iloc[day,exp] = len(alive_index)
        df_res_dead.iloc[day,exp] = len(dead_index)
        df_res_latent.iloc[day,exp] = len(latent_index)
        df_res_active.iloc[day,exp] = len(active_index)
        
        morbidity_iter = 1 - ((1-morbidity)**len(active_index))
        
        for i in alive_index:
            if np.random.binomial(1, morbidity_iter) == 1:
                df_iter.iloc[day+1,i] = 'latent_0'
            else:
                df_iter.iloc[day+1,i] = 'alive'
        
        for i in latent_index:
            num=int(regexp(df_iter.iloc[day,i])[1])
            if num<len(latent_rate):
                if np.random.binomial(1, latent_rate[num])==0:
                    next_num=num+1
                    df_iter.iloc[day+1,i] = 'latent_{}'.format(next_num)
                else: df_iter.iloc[day+1,i] = 'active_0'
            else: df_iter.iloc[day+1,i] = 'active_0'

        for i in active_index:
            if np.random.binomial(1, death_rate) == 1:
                df_iter.iloc[day+1,i] = 'dead'
            else:
                num=int(regexp(df_iter.iloc[day,i])[1])
                if num<len(active_rate):
                    if np.random.binomial(1, active_rate[num])==0:
                        next_num=num+1
                        df_iter.iloc[day+1,i]='active_{}'.format(next_num)
                    else: df_iter.iloc[day+1,i] = 'alive'
                else: df_iter.iloc[day+1,i] = 'alive'
 
        for i in dead_index:
            df_iter.iloc[day+1,i] = 'dead'
            
    alive_index = []
    latent_index = []
    active_index = []
    dead_index = []       

    for i in range(0, n_people):
        if regexp(df_iter.iloc[n_days-1,i])[0] == 'active':
            active_index.append(i) 
        if regexp(df_iter.iloc[n_days-1,i])[0] == 'alive':
            alive_index.append(i)    
        if regexp(df_iter.iloc[n_days-1,i])[0] == 'latent':
            latent_index.append(i)
        if regexp(df_iter.iloc[n_days-1,i])[0] == 'dead':
            dead_index.append(i)       
            
    df_res_alive.iloc[n_days-1,exp] = int(len(alive_index))
    df_res_dead.iloc[n_days-1,exp] = len(dead_index)
    df_res_latent.iloc[n_days-1,exp] = len(latent_index)
    df_res_active.iloc[n_days-1,exp] = len(active_index)
    
    for df in [df_res_alive, df_res_dead, df_res_latent, df_res_active]:
        df['avg'] = df.mean(axis=1)

f, axes = plt.subplots(4, figsize=(20, 15))
sns.barplot(x=df_res_alive.index, y=df_res_alive.avg, ax=axes[0]).set_title('ALIVE')
sns.barplot(x=df_res_latent.index, y=df_res_latent.avg, ax=axes[1]).set_title('LATENT')
sns.barplot(x=df_res_active.index, y=df_res_active.avg, ax=axes[2]).set_title('ACTIVE')
sns.barplot(x=df_res_dead.index, y=df_res_dead.avg, ax=axes[3]).set_title('DEAD')
for i in range(4):
    axes[i].set_ylim(0,n_people)
plt.savefig("plot.png") 

from statsmodels.stats.weightstats import _tconfint_generic

def conf_int(table, day, accuracy):
    titles=['alive', 'latent', 'active', 'dead']
    dict_tables={'alive':df_res_alive,
                 'latent':df_res_latent,
                 'active':df_res_active,
                 'dead':df_res_dead}             
    if table in titles:
        array = dict_tables[table].iloc[day, :-1].values
        mean_std = array.std(ddof=1)/np.sqrt(len(array))
        mean = array.mean()
        interval = _tconfint_generic(mean, mean_std,
                                len(array)-1, 0.05, 'two-sided')
        left, right =round(interval[0],accuracy), round(interval[1],accuracy)
        print('95% confidence interval for {} people in day №{}: ({}, {})'.format(table, day, left, right))
    else:
        print(f'You have to use one of this titles: {titles}')
        
#conf_int('alive', 25, 3)
