#!/usr/bin/env python
# coding: utf-8

# In[220]:


import pandas as pd
import numpy as np
from sklearn import linear_model
import statsmodels.api as sm


# In[221]:


cube = pd.read_excel(r'C:\Users\gobhuv\Desktop\Personal\APPC\cube.xlsx')
fleet = pd.read_excel(r'C:\Users\gobhuv\Desktop\Personal\APPC\Fleet size.xlsx')
hours = pd.read_excel(r'C:\Users\gobhuv\Desktop\Personal\APPC\hours.xlsx')
spozh = pd.read_excel(r'C:\Users\gobhuv\Desktop\Personal\APPC\SPOZH.xlsx')
vans = pd.read_excel(r'C:\Users\gobhuv\Desktop\Personal\APPC\Vans.xlsx')
volume = pd.read_excel(r'C:\Users\gobhuv\Desktop\Personal\APPC\Volume.xlsx')
zips = pd.read_excel(r'C:\Users\gobhuv\Desktop\Personal\APPC\Zips.xlsx')
time = pd.read_excel(r'C:\Users\gobhuv\Desktop\Personal\APPC\Time.xlsx')
small=50
standard=80
large=100


# In[222]:


x=spozh[['Volume']]
y=spozh['SPOZH']

# with sklearn
regr = linear_model.LinearRegression()
regr.fit(x, y)

print('Intercept: \n', regr.intercept_)
print('Coefficients: \n', regr.coef_)


# In[223]:


# with statsmodels
x = sm.add_constant(x) # adding a constant

model = sm.OLS(y, x).fit()
predictions = model.predict(x) 

print_model = model.summary()
print(print_model)


# In[224]:


v=volume
v['SPOZH']=pd.DataFrame(regr.predict(volume[['Volume']]))


# In[225]:


v_1=pd.merge(v,hours,on =['Station','Date'],how ='outer')
v_2=pd.merge(v_1,time,on =['Station'],how ='outer')


# In[226]:


v_2['TimeOut_SPR']=v_2.SPOZH*(v_2.Hours-2*v_2.in_out_bound_time)


# In[227]:


v_3=pd.merge(v_2,fleet,on =['Station'],how ='outer')


# In[228]:


v_4=pd.merge(v_3,cube,on =['Station','Date'],how ='outer')


# In[229]:


v_4['CubeOut_SPR']=((v_4['small']*small+v_4['standard']*standard+v_4['large']*large)/(v_4['small']+v_4['standard']+v_4['large']))/v_4['Cube']


# In[230]:


v_4['SPR']=pd.DataFrame([v_4['TimeOut_SPR'],v_4['CubeOut_SPR']]).min()


# In[231]:


v_5=pd.merge(v_4,vans,on =['Station','Date'],how ='outer')


# In[232]:


v_5['Routes_Needed']=v_5['Volume']/v_5['SPR']


# In[233]:


v_5['diff']=v_5['Routes_Needed']-v_5['Routes']


# In[234]:


v_5['Additional_Routes_Needed']=v_5['diff'].apply(lambda x: x if x >0 else 0)


# In[235]:


v_5=v_5.drop('diff', axis=1)


# In[236]:


v_5


# In[ ]:




