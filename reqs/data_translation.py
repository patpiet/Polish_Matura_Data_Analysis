#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
from itranslate import itranslate as itrans

df_results = pd.read_csv('matura_results.csv')


# In[6]:


# Could use that on only one column as there are limited restriction in the google API
df_results['przedmiot'] = df_results['przedmiot'].apply(lambda x: itrans(x, from_lang='pl', to_lang='en'))
df_results


# In[9]:


# Translate columns
df_results.drop(['rodzaj_egzaminu'], axis=1, inplace=True)
df_results.columns = ['level', 'subject', 'gender', 'year', 'value_perc']


# In[11]:


df_results['level'].value_counts()


# In[13]:


# Translate level cell
df_results['level'] =df_results['level'].apply(lambda x: 'Advanced' if x =='rozszerzony' else 'Basic')


# In[14]:


df_results['gender'].value_counts()


# In[15]:


# Translates gender column
def translate_gender(gender):
    if gender == 'kobiety':
        return 'Women'
    elif gender =='mężczyźni':
        return 'Men'
    else:
        return 'Altogether'
    
df_results['gender'] = df_results['gender'].apply(translate_gender)
df_results


# In[16]:


df_results['subject'].value_counts()


# In[17]:


# Delete language key word from subjects' name
# Capitalize the subject names
df_results['subject'] = df_results['subject'].apply(lambda x: x.replace('language', ''))
df_results['subject'] = df_results['subject'].apply(lambda x: x.capitalize())
df_results['subject'].value_counts()


# In[37]:


# SECOND FILE
df_region = pd.read_csv('matura_region_ratio.csv')
df_region


# In[24]:


try:
    df_region['region_en'] = df_region['wojewodztwo'].apply(lambda x: itrans(x, from_lang='pl', to_lang='en'))
except ValueError:
    continue


# In[38]:


df_region['region_en'] = en
df_region


# In[39]:


df_region.columns = ['region_pl', 'gender', 'year', 'ratio', 'region_en']
df_region['gender'] = df_region['gender'].apply(translate_gender)


# In[40]:


df_region['gender'].value_counts()


# In[36]:


en = df_region['region_en']


# In[ ]:




