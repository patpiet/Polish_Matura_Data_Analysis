#!/usr/bin/env python
# coding: utf-8

# In[118]:


import pandas as pd
import numpy as np

# delete columns that are not needed
# cast value to integer
# Create the column with ratio of students who passed in each polish region


# In[139]:


df_results = pd.read_csv('srednie_wyniki_egzaminu_maturalnego_2.csv', sep=';').drop(['nazwa_zmiennej', 
                                                                        'flaga', 'typ_informacji_z_jednostka_miary'], axis=1)
df_results.shape


# In[140]:


df_results.dtypes


# In[141]:


df_results.columns


# In[142]:


df_results['wartosc'] = df_results['wartosc'].astype(str)
df_results['wartosc'] = df_results['wartosc'].apply(lambda x: float(x.replace(',','.')))
df_results.dtypes


# In[146]:


df_students = pd.read_csv('liczba_osob_ktore_przystapily_lub_zdaly_egzamin_maturalny.csv', sep=';').drop(['nazwa_zmiennej', 
                                                                        'flaga', 'typ_informacji_z_jednostka_miary', 'kraj'], axis=1)
df_students.shape


# In[147]:


df_students


# In[148]:


df_students.dtypes


# In[172]:


df_passed = df_students[df_students['status_zdajacych'] == 'zdało']
df_participated = df_students[df_students['status_zdajacych'] == 'przystąpiło']


# In[192]:


new_list = []


for index, row in df_participated.iterrows():
    passed = df_passed[ (df_passed['wojewodztwo'] == row['wojewodztwo']) & (df_passed['plec'] == row['plec'])
                         & (df_passed['rok'] == row['rok']) ]['wartosc'].values
    ratio = passed[0] / row['wartosc']
    new_dir = {'wojewodztwo': row['wojewodztwo'], 'plec': row['plec'], 'rok': row['rok'], 'ratio': ratio}
    new_list.append(new_dir)
    
df_region_with_ratio = pd.DataFrame(new_list)
df_region_with_ratio


# In[191]:


# Lets sort with just oral type of exam
df_results = df_results[df_results['rodzaj_egzaminu'] == 'pisemny']
df_results


# In[195]:


# from itranslate import itranslate as itrans

# df_results['przedmiot'] = df_results['przedmiot'].apply(lambda x: itrans(x, from_lang='pl',to_lang='en',))


# In[198]:


df_results.to_csv('matura_results.csv', index=False)


# In[200]:


df_region_with_ratio.to_csv('matura_region_ratio.csv', index=False)


# In[ ]:




