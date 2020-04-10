import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('RostVesStud.csv', index_col='2018')

data=data[:-1].fillna(0)

data=data.astype('int')

data['TotalF']=data[['IASA(F)', 'FMF(F)', 'ITC(F)']].sum(axis=1)
data['TotalM']=data[['IASA(M)', 'FMF(M)', 'ITC(M)']].sum(axis=1)

indexes=list(data.index)
heights_male=list(data['TotalM'])

non_null_indexes_male=[]
non_null_heights_male=[]

for i in range(len(indexes)):
    if heights_male[i]!=0:
        non_null_indexes_male.append(int(indexes[i]))
        non_null_heights_male.append(heights_male[i])

heights_female=list(data['TotalF'])

non_null_indexes_female=[]
non_null_heights_female=[]


for i in range(len(indexes)):
    if heights_female[i]!=0:
        non_null_indexes_female.append(int(indexes[i]))
        non_null_heights_female.append(heights_female[i])
'''
f, axes = plt.subplots(2, figsize=(10, 10))
sns.barplot(x=non_null_indexes_male, y=non_null_heights_male,
            ax=axes[0], color='dodgerblue').set_title('Male height distribution')
sns.barplot(x=non_null_indexes_female, y=non_null_heights_female,
            ax=axes[1],color='fuchsia').set_title('Female height distribution')
'''
statistical_array_male=[]
for i in range(len(non_null_heights_male)):
    for y in range(non_null_heights_male[i]):
        statistical_array_male.append(non_null_indexes_male[i])
        
statistical_array_female=[]
for i in range(len(non_null_heights_female)):
    for y in range(non_null_heights_female[i]):
        statistical_array_female.append(non_null_indexes_female[i])
        
q1_m=np.quantile(statistical_array_male, 0.1)
q9_m=np.quantile(statistical_array_male, 0.9)

q1_f=np.quantile(statistical_array_female, 0.1)
q9_f=np.quantile(statistical_array_female, 0.9)

median_m=np.median(statistical_array_male)
median_f=np.median(statistical_array_female)

mean_m=np.mean(statistical_array_male)
mean_f=np.mean(statistical_array_female)

std_m=np.std(statistical_array_male)
std_f=np.std(statistical_array_female)

print('Quantile p=0.1: male = {}, female = {}'.format(q1_m, q1_f))
print('Quantile p=0.9: male = {}, female = {}'.format(q9_m, q9_f))
print('Median: male = {}, female = {}'.format(median_m, median_f))
print('Mean: male = {}, female = {}'.format(mean_m, mean_f))
print('Std: male = {}, female = {}'.format(std_m, std_f))