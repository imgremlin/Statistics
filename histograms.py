import matplotlib.pyplot as plt
import random
import seaborn as sns

exp=[]
uni=[]
norm=[]

for i in range(1000):
    exp.append(random.expovariate(2))
    uni.append(random.uniform(-1,3))
    norm.append(random.normalvariate(1,2))

f, axes = plt.subplots(2, 3, figsize=(12, 12))
f.suptitle('Exp(1)', fontsize=20)
sns.distplot(exp, kde=False, bins=5, ax=axes[0][0]).set_title('5 bins')
sns.distplot(exp, kde=False, bins=10, ax=axes[0][1]).set_title('10 bins')
sns.distplot(exp, kde=False, bins=20, ax=axes[0][2]).set_title('20 bins')
sns.distplot(exp, kde=False, bins=50, ax=axes[1][0]).set_title('50 bins')
sns.distplot(exp, kde=False, bins=70, ax=axes[1][1]).set_title('70 bins')
sns.distplot(exp, kde=False, bins=100, ax=axes[1][2]).set_title('100 bins')

f1, axes1 = plt.subplots(2, 3, figsize=(12, 12))
f1.suptitle('U(−1, 3)', fontsize=20)
sns.distplot(uni, kde=False, bins=5, ax=axes1[0][0]).set_title('5 bins')
sns.distplot(uni, kde=False, bins=10, ax=axes1[0][1]).set_title('10 bins')
sns.distplot(uni, kde=False, bins=20, ax=axes1[0][2]).set_title('20 bins')
sns.distplot(uni, kde=False, bins=50, ax=axes1[1][0]).set_title('50 bins')
sns.distplot(uni, kde=False, bins=70, ax=axes1[1][1]).set_title('70 bins')
sns.distplot(uni, kde=False, bins=100, ax=axes1[1][2]).set_title('100 bins')

f2, axes2 = plt.subplots(2, 3, figsize=(12, 12))
f2.suptitle('N(1, 4)', fontsize=20)
sns.distplot(norm, kde=False, bins=5, ax=axes2[0][0]).set_title('5 bins')
sns.distplot(norm, kde=False, bins=10, ax=axes2[0][1]).set_title('10 bins')
sns.distplot(norm, kde=False, bins=20, ax=axes2[0][2]).set_title('20 bins')
sns.distplot(norm, kde=False, bins=50, ax=axes2[1][0]).set_title('50 bins')
sns.distplot(norm, kde=False, bins=70, ax=axes2[1][1]).set_title('70 bins')
sns.distplot(norm, kde=False, bins=100, ax=axes2[1][2]).set_title('100 bins')

