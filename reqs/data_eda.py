#!/usr/bin/env python
# coding: utf-8

# In[274]:


# Understand the data
## how results changed over years
## what are strong and weak subjects for students
## performance on science, numerical and humanistic subjects
## gap between advanced and basic level 
# Visualize the data
# Create a dropdown for categories
# Create map of Poland with the passed exams ratio


# In[261]:


import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt


# In[330]:


df_results = pd.read_csv('Data/matura_results.csv')


# In[335]:


# The scores are stable with slight down-trend
plt.figure()

pd.pivot_table(df_results, values='value_perc', index='year', columns='level').plot(kind='bar', figsize=(10,5))

plt.ylim(0,100)
plt.xlabel('Year')
plt.ylabel('Average Score (%)')
plt.legend(loc='best')
plt.title('Average Score Over Years')
plt.xticks(rotation=0)


# In[86]:


pd.pivot_table(df_results, values='value_perc', index='year', columns='gender')


# In[91]:


pd.pivot_table(df_results, values='value_perc', columns='gender', index='subject').sort_values('Men')


# In[94]:


# Looks like Lemko is not popular subject at all
# We need to fill these 0 with mean value of each gender from years where it was not 0
df_results[df_results['value_perc'] == 0]


# In[198]:


# change 0 value to np.nan
df_results['value_perc'] = df_results['value_perc'].apply(lambda x: np.nan if x == 0 else x)

# get mean of each gender of Lamko subject
mean_men = df_results[ (df_results['value_perc'] != 0) & (df_results['gender'] == 'Men') & 
                      (df_results['subject'] == 'Lemko ')]['value_perc'].mean()

mean_women = df_results[ (df_results['value_perc'] != 0) & (df_results['gender'] == 'Women') & 
                      (df_results['subject'] == 'Lemko ')]['value_perc'].mean()

mean_altogether = df_results[ (df_results['value_perc'] != 0) & (df_results['gender'] == 'Altogether') & 
                      (df_results['subject'] == 'Lemko ')]['value_perc'].mean()

# fill na with mean
df_results.loc[df_results['gender'] == 'Men', 'value_perc'] = df_results[df_results['gender'] == 'Men']['value_perc'].fillna(mean_men)
df_results.loc[df_results['gender'] == 'Women', 'value_perc'] = df_results[df_results['gender'] == 'Women']['value_perc'].fillna(mean_women)
df_results.loc[df_results['gender'] == 'Altogether', 'value_perc'] = df_results[df_results['gender'] == 'Altogether']['value_perc'].fillna(mean_altogether)


# In[331]:


# Languages obviously dominate
pd.pivot_table(df_results[df_results['level'] == 'Advanced'], 
               values='value_perc', columns='gender', index='subject').sort_values('Men', ascending=False)


# In[156]:


# Lets group the subjects into 'languages', 'science' and 'humanistic' subjects

languages = ['Lemko ', 'Belarusian', 'Italian ', 'Lithuanian ', 'Ukrainian ',
       'French', 'Spanish ', 'English', 'Russian', 'German',
       'Latin and ancient culture', 'Kashubian',]
sciences = ['Chemistry', 'Maths', 'Physics', 'Biology', 'Informatics', 'Geography']
humanistic = ['Polish ', 'History of music', 'Philosophy', 'History of art', 'History', 'Civics']

def get_catg(subject):
    if subject in languages:
        return 'Languages'
    elif subject in sciences:
        return 'Sciences'
    elif subject in humanistic:
        return 'Humanistic'
    else:
        return np.nan


# In[157]:


df_results['category'] = df_results['subject'].apply(get_catg)


# In[229]:


plt.figure()
pd.pivot_table(df_results[(df_results['level'] == 'Advanced') & (df_results['gender'] == 'Altogether')], 
               values='value_perc', columns='gender', index='category').sort_values('Altogether', ascending=False).plot(kind='bar')

plt.xticks(rotation=0)
plt.ylabel('Avg Score (%)')
plt.xlabel('')
plt.title('Average Score by Category (Advanced Level)')
plt.ylim([0, 100])
plt.legend().remove()


# In[287]:


# Let's compare most common subjects at basic and advance levels

df_common = df_results[ (df_results['subject'] == 'Polish ') |
                      (df_results['subject'] == 'Maths') |
                      (df_results['subject'] == 'English')]

plt.figure()
pd.pivot_table(df_common, values='value_perc', columns='level', index='subject').sort_values('Basic', ascending=False).plot(kind='bar')

plt.xticks(rotation=0)
plt.xlabel('')
plt.title('Most Common Subjects Score by level')
plt.ylabel('Avg Score (%)')
plt.legend(['Advanced', 'Basic'])
# print(plt.bar_label())
common_plt = plt.gca()


# In[327]:


# Let's compare most common subjects at basic and advance levels

for level in df_results['level'].unique():    
    df_common = df_results[ (df_results['subject'] == 'Polish ') |
                          (df_results['subject'] == 'Maths') |
                          (df_results['subject'] == 'English')]
    df_common = df_common[df_common['gender'] != 'Altogether']
    df_common = df_common[df_common['level'] == level]
    
    plt.figure()
    pd.pivot_table(df_common, values='value_perc', columns='gender', index='subject').plot(kind='bar')

    plt.xticks(rotation=0)
    plt.xlabel('')
    plt.title('Most Common Subjects by Gender ({} level)'.format(level))
    plt.ylabel('Avg Score (%)')
    plt.ylim(0,100)
    # plt.legend(['Advanced', 'Basic'])
    common_plt = plt.gca()


# In[277]:


df_results.to_csv('matura_results.csv')


# In[ ]:




