
# Machine Learning 
## Random Forest - Regresion Logistica - Analisis Discriminante - K vecinos - Arboles de Decision - SVM - Gaussian NB


```python
import sys
print('Python: {}'.format(sys.version))
# scipy
import scipy
print('scipy: {}'.format(scipy.__version__))
# numpy
import numpy
print('numpy: {}'.format(numpy.__version__))
# matplotlib
import matplotlib
print('matplotlib: {}'.format(matplotlib.__version__))
# pandas
import pandas as pd
print('pandas: {}'.format(pd.__version__))
# scikit-learn
import sklearn
print('sklearn: {}'.format(sklearn.__version__))
# pymongo
import pymongo
print('pymongo: {}'.format(pymongo.__version__))
```

    Python: 3.6.4 |Anaconda, Inc.| (default, Jan 16 2018, 10:22:32) [MSC v.1900 64 bit (AMD64)]
    scipy: 1.0.1
    numpy: 1.14.2
    matplotlib: 2.2.2
    pandas: 0.23.0
    sklearn: 0.19.1
    pymongo: 3.4.0
    


```python
import warnings
warnings.filterwarnings('ignore')
```


```python
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
# from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn import preprocessing
from pymongo import MongoClient
```

# Cargamos los datos

### Usando MongoDB


```python
client = MongoClient('localhost', 27017)
db = client.datascience
collection = db.incidents
```

#### - Usamos un cursor para construir el Dataframe


```python
cursor = collection.find()
incidents = pd.DataFrame(list(cursor))
```

#### - Borramos el _id que Mongo genera automáticamente



```python
 if no_id:
     del incidents['_id']

 return incidents
```

### Usando un csv


```python
names = ['category', 'type', 'dayofweek', 'date', 'time','day','year','month','hour','district', 'resolution', 'latitude', 'longitude']
incidents = pd.read_csv("Incidents.all.ml.csv", names=names, sep=';')
```

### Cargaremos un csv de 2017-18 (menos datos)


```python
names = ['category', 'type', 'dayofweek', 'date', 'time','day','year','month','hour','district', 'resolution', 'latitude', 'longitude']
incidents = pd.read_csv("Incidents.red.ml.csv", names=names, sep=';')
```

## shape. Dimensiones del conjunto de datos


```python
print(incidents.shape)
```

    (915339, 13)
    

## head


```python
incidents.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>category</th>
      <th>type</th>
      <th>dayofweek</th>
      <th>date</th>
      <th>time</th>
      <th>day</th>
      <th>year</th>
      <th>month</th>
      <th>hour</th>
      <th>district</th>
      <th>resolution</th>
      <th>latitude</th>
      <th>longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>VANDALISM</td>
      <td>MALICIOUS MISCHIEF</td>
      <td>Monday</td>
      <td>2007-10-22</td>
      <td>14:30:00</td>
      <td>22</td>
      <td>2007</td>
      <td>10</td>
      <td>14</td>
      <td>TARAVAL</td>
      <td>NONE</td>
      <td>-122.466758005159</td>
      <td>37.729185</td>
    </tr>
    <tr>
      <th>1</th>
      <td>OTHER OFFENSES</td>
      <td>RESISTING ARREST</td>
      <td>Sunday</td>
      <td>2008-03-02</td>
      <td>21:31:00</td>
      <td>02</td>
      <td>2008</td>
      <td>3</td>
      <td>21</td>
      <td>TENDERLOIN</td>
      <td>ARREST, BOOKED</td>
      <td>-122.412224164736</td>
      <td>37.782073</td>
    </tr>
    <tr>
      <th>2</th>
      <td>VANDALISM</td>
      <td>MALICIOUS MISCHIEF, VANDALISM OF VEHICLES</td>
      <td>Friday</td>
      <td>2009-10-30</td>
      <td>19:30:00</td>
      <td>30</td>
      <td>2009</td>
      <td>10</td>
      <td>19</td>
      <td>NORTHERN</td>
      <td>NONE</td>
      <td>-122.422253466945</td>
      <td>37.790863</td>
    </tr>
    <tr>
      <th>3</th>
      <td>OTHER OFFENSES</td>
      <td>PROBATION VIOLATION</td>
      <td>Wednesday</td>
      <td>2011-01-19</td>
      <td>16:25:00</td>
      <td>19</td>
      <td>2011</td>
      <td>1</td>
      <td>16</td>
      <td>INGLESIDE</td>
      <td>ARREST, BOOKED</td>
      <td>-122.447125045686</td>
      <td>37.721031</td>
    </tr>
    <tr>
      <th>4</th>
      <td>NON-CRIMINAL</td>
      <td>AIDED CASE, MENTAL DISTURBED</td>
      <td>Friday</td>
      <td>2008-09-12</td>
      <td>13:21:00</td>
      <td>12</td>
      <td>2008</td>
      <td>9</td>
      <td>13</td>
      <td>MISSION</td>
      <td>PSYCHOPATHIC CASE</td>
      <td>-122.416954468807</td>
      <td>37.753880</td>
    </tr>
    <tr>
      <th>5</th>
      <td>NON-CRIMINAL</td>
      <td>LOST PROPERTY</td>
      <td>Thursday</td>
      <td>2003-10-02</td>
      <td>21:00:00</td>
      <td>02</td>
      <td>2003</td>
      <td>10</td>
      <td>21</td>
      <td>RICHMOND</td>
      <td>NONE</td>
      <td>-122.472843756561</td>
      <td>37.780629</td>
    </tr>
    <tr>
      <th>6</th>
      <td>LARCENY/THEFT</td>
      <td>GRAND THEFT OF PROPERTY</td>
      <td>Monday</td>
      <td>2005-02-07</td>
      <td>18:50:00</td>
      <td>07</td>
      <td>2005</td>
      <td>2</td>
      <td>18</td>
      <td>MISSION</td>
      <td>ARREST, BOOKED</td>
      <td>-122.418596727467</td>
      <td>37.753838</td>
    </tr>
    <tr>
      <th>7</th>
      <td>VEHICLE THEFT</td>
      <td>STOLEN AND RECOVERED VEHICLE</td>
      <td>Tuesday</td>
      <td>2006-08-22</td>
      <td>18:30:00</td>
      <td>22</td>
      <td>2006</td>
      <td>8</td>
      <td>18</td>
      <td>CENTRAL</td>
      <td>NONE</td>
      <td>-122.400439442308</td>
      <td>37.795223</td>
    </tr>
    <tr>
      <th>8</th>
      <td>VEHICLE THEFT</td>
      <td>STOLEN AUTOMOBILE</td>
      <td>Thursday</td>
      <td>2012-10-04</td>
      <td>17:00:00</td>
      <td>04</td>
      <td>2012</td>
      <td>10</td>
      <td>17</td>
      <td>INGLESIDE</td>
      <td>NONE</td>
      <td>-122.405527956606</td>
      <td>37.716948</td>
    </tr>
    <tr>
      <th>9</th>
      <td>OTHER OFFENSES</td>
      <td>OBSCENE PHONE CALLS(S)</td>
      <td>Wednesday</td>
      <td>2010-11-17</td>
      <td>18:30:00</td>
      <td>17</td>
      <td>2010</td>
      <td>11</td>
      <td>18</td>
      <td>RICHMOND</td>
      <td>NONE</td>
      <td>-122.459722209477</td>
      <td>37.778342</td>
    </tr>
  </tbody>
</table>
</div>



## Statistical summary. descriptions


```python
incidents.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>year</th>
      <th>month</th>
      <th>hour</th>
      <th>longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>915339.000000</td>
      <td>915339.000000</td>
      <td>915339.000000</td>
      <td>915339.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>2001.726924</td>
      <td>16.591035</td>
      <td>13.410482</td>
      <td>36.959908</td>
    </tr>
    <tr>
      <th>std</th>
      <td>141.713059</td>
      <td>142.234680</td>
      <td>6.518946</td>
      <td>11.370903</td>
    </tr>
    <tr>
      <th>min</th>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>-122.513642</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>2007.000000</td>
      <td>3.000000</td>
      <td>9.000000</td>
      <td>37.753565</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>2013.000000</td>
      <td>6.000000</td>
      <td>14.000000</td>
      <td>37.775421</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>2016.000000</td>
      <td>10.000000</td>
      <td>19.000000</td>
      <td>37.784666</td>
    </tr>
    <tr>
      <th>max</th>
      <td>2018.000000</td>
      <td>2018.000000</td>
      <td>23.000000</td>
      <td>90.000000</td>
    </tr>
  </tbody>
</table>
</div>



## Class Distribution


```python
incidents.groupby('category').size()
```




    category
    ARSON                            1656
    ASSAULT                         79695
    BAD CHECKS                        352
    BRIBERY                           350
    BURGLARY                        36699
    DISORDERLY CONDUCT               3876
    DRIVING UNDER THE INFLUENCE      2221
    DRUG/NARCOTIC                   42692
    DRUNKENNESS                      3502
    EMBEZZLEMENT                     1149
    EXTORTION                         335
    FAMILY OFFENSES                   415
    FORGERY/COUNTERFEITING           8105
    FRAUD                           16474
    GAMBLING                          146
    KIDNAPPING                       1881
    LARCENY/THEFT                  223943
    LIQUOR LAWS                      1466
    LOITERING                         846
    MISSING PERSON                  26037
    NON-CRIMINAL                    98777
    OTHER OFFENSES                 122214
    PORNOGRAPHY/OBSCENE MAT            26
    PROSTITUTION                     5961
    RECOVERED VEHICLE                3729
    ROBBERY                         21983
    RUNAWAY                          1692
    SECONDARY CODES                 10715
    SEX OFFENSES, FORCIBLE           5088
    SEX OFFENSES, NON FORCIBLE        190
    STOLEN PROPERTY                  4839
    SUICIDE                           514
    SUSPICIOUS OCC                  33321
    TREA                                7
    TRESPASS                         8614
    VANDALISM                       50563
    VEHICLE THEFT                   47440
    WARRANTS                        38581
    WEAPON LAWS                      9245
    dtype: int64



* Descarte de las columnas para realizar una mejor discretación de los atributos para realizar la clasificación


```python
dataset = incidents.copy()
dataset.drop(dataset.columns[[1,3,4,5,6,7]], axis=1, inplace=True)
```


```python
incidents.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>category</th>
      <th>type</th>
      <th>dayofweek</th>
      <th>date</th>
      <th>time</th>
      <th>day</th>
      <th>year</th>
      <th>month</th>
      <th>hour</th>
      <th>district</th>
      <th>resolution</th>
      <th>latitude</th>
      <th>longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>VANDALISM</td>
      <td>MALICIOUS MISCHIEF</td>
      <td>Monday</td>
      <td>2007-10-22</td>
      <td>14:30:00</td>
      <td>22</td>
      <td>2007</td>
      <td>10</td>
      <td>14</td>
      <td>TARAVAL</td>
      <td>NONE</td>
      <td>-122.466758005159</td>
      <td>37.729185</td>
    </tr>
    <tr>
      <th>1</th>
      <td>OTHER OFFENSES</td>
      <td>RESISTING ARREST</td>
      <td>Sunday</td>
      <td>2008-03-02</td>
      <td>21:31:00</td>
      <td>02</td>
      <td>2008</td>
      <td>3</td>
      <td>21</td>
      <td>TENDERLOIN</td>
      <td>ARREST, BOOKED</td>
      <td>-122.412224164736</td>
      <td>37.782073</td>
    </tr>
    <tr>
      <th>2</th>
      <td>VANDALISM</td>
      <td>MALICIOUS MISCHIEF, VANDALISM OF VEHICLES</td>
      <td>Friday</td>
      <td>2009-10-30</td>
      <td>19:30:00</td>
      <td>30</td>
      <td>2009</td>
      <td>10</td>
      <td>19</td>
      <td>NORTHERN</td>
      <td>NONE</td>
      <td>-122.422253466945</td>
      <td>37.790863</td>
    </tr>
    <tr>
      <th>3</th>
      <td>OTHER OFFENSES</td>
      <td>PROBATION VIOLATION</td>
      <td>Wednesday</td>
      <td>2011-01-19</td>
      <td>16:25:00</td>
      <td>19</td>
      <td>2011</td>
      <td>1</td>
      <td>16</td>
      <td>INGLESIDE</td>
      <td>ARREST, BOOKED</td>
      <td>-122.447125045686</td>
      <td>37.721031</td>
    </tr>
    <tr>
      <th>4</th>
      <td>NON-CRIMINAL</td>
      <td>AIDED CASE, MENTAL DISTURBED</td>
      <td>Friday</td>
      <td>2008-09-12</td>
      <td>13:21:00</td>
      <td>12</td>
      <td>2008</td>
      <td>9</td>
      <td>13</td>
      <td>MISSION</td>
      <td>PSYCHOPATHIC CASE</td>
      <td>-122.416954468807</td>
      <td>37.753880</td>
    </tr>
  </tbody>
</table>
</div>




```python
dataset.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>category</th>
      <th>dayofweek</th>
      <th>hour</th>
      <th>district</th>
      <th>resolution</th>
      <th>latitude</th>
      <th>longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>VANDALISM</td>
      <td>Monday</td>
      <td>14</td>
      <td>TARAVAL</td>
      <td>NONE</td>
      <td>-122.466758005159</td>
      <td>37.729185</td>
    </tr>
    <tr>
      <th>1</th>
      <td>OTHER OFFENSES</td>
      <td>Sunday</td>
      <td>21</td>
      <td>TENDERLOIN</td>
      <td>ARREST, BOOKED</td>
      <td>-122.412224164736</td>
      <td>37.782073</td>
    </tr>
    <tr>
      <th>2</th>
      <td>VANDALISM</td>
      <td>Friday</td>
      <td>19</td>
      <td>NORTHERN</td>
      <td>NONE</td>
      <td>-122.422253466945</td>
      <td>37.790863</td>
    </tr>
    <tr>
      <th>3</th>
      <td>OTHER OFFENSES</td>
      <td>Wednesday</td>
      <td>16</td>
      <td>INGLESIDE</td>
      <td>ARREST, BOOKED</td>
      <td>-122.447125045686</td>
      <td>37.721031</td>
    </tr>
    <tr>
      <th>4</th>
      <td>NON-CRIMINAL</td>
      <td>Friday</td>
      <td>13</td>
      <td>MISSION</td>
      <td>PSYCHOPATHIC CASE</td>
      <td>-122.416954468807</td>
      <td>37.753880</td>
    </tr>
  </tbody>
</table>
</div>



## Normalización de datos


```python
ndataset = dataset.copy()
ndataset.district = pd.Categorical(ndataset.district)
ndataset.dayofweek = pd.Categorical(ndataset.dayofweek)
ndataset.resolution = pd.Categorical(ndataset.resolution)
ndataset.category = pd.Categorical(ndataset.category)

ndataset['district'] = ndataset.district.cat.codes
ndataset['dayofweek'] = ndataset.dayofweek.cat.codes
ndataset['resolution'] = ndataset.resolution.cat.codes
ndataset['category'] = ndataset.category.cat.codes

ndataset.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>category</th>
      <th>dayofweek</th>
      <th>hour</th>
      <th>district</th>
      <th>resolution</th>
      <th>latitude</th>
      <th>longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>35</td>
      <td>4</td>
      <td>14</td>
      <td>32</td>
      <td>15</td>
      <td>-122.466758005159</td>
      <td>37.729185</td>
    </tr>
    <tr>
      <th>1</th>
      <td>21</td>
      <td>8</td>
      <td>21</td>
      <td>33</td>
      <td>0</td>
      <td>-122.412224164736</td>
      <td>37.782073</td>
    </tr>
    <tr>
      <th>2</th>
      <td>35</td>
      <td>2</td>
      <td>19</td>
      <td>28</td>
      <td>15</td>
      <td>-122.422253466945</td>
      <td>37.790863</td>
    </tr>
    <tr>
      <th>3</th>
      <td>21</td>
      <td>11</td>
      <td>16</td>
      <td>26</td>
      <td>0</td>
      <td>-122.447125045686</td>
      <td>37.721031</td>
    </tr>
    <tr>
      <th>4</th>
      <td>20</td>
      <td>2</td>
      <td>13</td>
      <td>27</td>
      <td>21</td>
      <td>-122.416954468807</td>
      <td>37.753880</td>
    </tr>
  </tbody>
</table>
</div>




```python
ndataset = ndataset.convert_objects(convert_numeric=True).dropna()
ndataset
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>category</th>
      <th>dayofweek</th>
      <th>hour</th>
      <th>district</th>
      <th>resolution</th>
      <th>latitude</th>
      <th>longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>35</td>
      <td>4</td>
      <td>14</td>
      <td>32</td>
      <td>15</td>
      <td>-122.466758</td>
      <td>37.729185</td>
    </tr>
    <tr>
      <th>1</th>
      <td>21</td>
      <td>8</td>
      <td>21</td>
      <td>33</td>
      <td>0</td>
      <td>-122.412224</td>
      <td>37.782073</td>
    </tr>
    <tr>
      <th>2</th>
      <td>35</td>
      <td>2</td>
      <td>19</td>
      <td>28</td>
      <td>15</td>
      <td>-122.422253</td>
      <td>37.790863</td>
    </tr>
    <tr>
      <th>3</th>
      <td>21</td>
      <td>11</td>
      <td>16</td>
      <td>26</td>
      <td>0</td>
      <td>-122.447125</td>
      <td>37.721031</td>
    </tr>
    <tr>
      <th>4</th>
      <td>20</td>
      <td>2</td>
      <td>13</td>
      <td>27</td>
      <td>21</td>
      <td>-122.416954</td>
      <td>37.753880</td>
    </tr>
    <tr>
      <th>5</th>
      <td>20</td>
      <td>9</td>
      <td>21</td>
      <td>30</td>
      <td>15</td>
      <td>-122.472844</td>
      <td>37.780629</td>
    </tr>
    <tr>
      <th>6</th>
      <td>16</td>
      <td>4</td>
      <td>18</td>
      <td>27</td>
      <td>0</td>
      <td>-122.418597</td>
      <td>37.753838</td>
    </tr>
    <tr>
      <th>7</th>
      <td>36</td>
      <td>10</td>
      <td>18</td>
      <td>25</td>
      <td>15</td>
      <td>-122.400439</td>
      <td>37.795223</td>
    </tr>
    <tr>
      <th>8</th>
      <td>36</td>
      <td>9</td>
      <td>17</td>
      <td>26</td>
      <td>15</td>
      <td>-122.405528</td>
      <td>37.716948</td>
    </tr>
    <tr>
      <th>9</th>
      <td>21</td>
      <td>11</td>
      <td>18</td>
      <td>30</td>
      <td>15</td>
      <td>-122.459722</td>
      <td>37.778342</td>
    </tr>
    <tr>
      <th>10</th>
      <td>20</td>
      <td>4</td>
      <td>9</td>
      <td>27</td>
      <td>19</td>
      <td>-122.418055</td>
      <td>37.753924</td>
    </tr>
    <tr>
      <th>11</th>
      <td>21</td>
      <td>9</td>
      <td>20</td>
      <td>31</td>
      <td>0</td>
      <td>-122.406892</td>
      <td>37.782483</td>
    </tr>
    <tr>
      <th>12</th>
      <td>32</td>
      <td>4</td>
      <td>23</td>
      <td>26</td>
      <td>15</td>
      <td>-122.429802</td>
      <td>37.730382</td>
    </tr>
    <tr>
      <th>13</th>
      <td>32</td>
      <td>4</td>
      <td>12</td>
      <td>24</td>
      <td>15</td>
      <td>-122.386619</td>
      <td>37.732467</td>
    </tr>
    <tr>
      <th>14</th>
      <td>37</td>
      <td>2</td>
      <td>23</td>
      <td>33</td>
      <td>0</td>
      <td>-122.409500</td>
      <td>37.785284</td>
    </tr>
    <tr>
      <th>15</th>
      <td>16</td>
      <td>7</td>
      <td>23</td>
      <td>32</td>
      <td>15</td>
      <td>-122.460302</td>
      <td>37.724209</td>
    </tr>
    <tr>
      <th>16</th>
      <td>20</td>
      <td>4</td>
      <td>8</td>
      <td>31</td>
      <td>15</td>
      <td>-122.403405</td>
      <td>37.775421</td>
    </tr>
    <tr>
      <th>17</th>
      <td>35</td>
      <td>4</td>
      <td>21</td>
      <td>31</td>
      <td>15</td>
      <td>-122.396533</td>
      <td>37.778327</td>
    </tr>
    <tr>
      <th>18</th>
      <td>16</td>
      <td>11</td>
      <td>20</td>
      <td>27</td>
      <td>15</td>
      <td>-122.410811</td>
      <td>37.751091</td>
    </tr>
    <tr>
      <th>19</th>
      <td>37</td>
      <td>2</td>
      <td>12</td>
      <td>26</td>
      <td>0</td>
      <td>-122.446607</td>
      <td>37.720723</td>
    </tr>
    <tr>
      <th>20</th>
      <td>20</td>
      <td>7</td>
      <td>15</td>
      <td>29</td>
      <td>21</td>
      <td>-122.440880</td>
      <td>37.777532</td>
    </tr>
    <tr>
      <th>21</th>
      <td>19</td>
      <td>10</td>
      <td>18</td>
      <td>27</td>
      <td>15</td>
      <td>-122.439794</td>
      <td>37.753313</td>
    </tr>
    <tr>
      <th>22</th>
      <td>16</td>
      <td>11</td>
      <td>12</td>
      <td>28</td>
      <td>15</td>
      <td>-122.429950</td>
      <td>37.782742</td>
    </tr>
    <tr>
      <th>23</th>
      <td>20</td>
      <td>9</td>
      <td>13</td>
      <td>25</td>
      <td>15</td>
      <td>-122.417273</td>
      <td>37.786149</td>
    </tr>
    <tr>
      <th>24</th>
      <td>7</td>
      <td>2</td>
      <td>17</td>
      <td>26</td>
      <td>1</td>
      <td>-122.415291</td>
      <td>37.713504</td>
    </tr>
    <tr>
      <th>25</th>
      <td>8</td>
      <td>4</td>
      <td>19</td>
      <td>33</td>
      <td>0</td>
      <td>-122.416711</td>
      <td>37.783357</td>
    </tr>
    <tr>
      <th>26</th>
      <td>21</td>
      <td>11</td>
      <td>17</td>
      <td>24</td>
      <td>0</td>
      <td>-122.390972</td>
      <td>37.734015</td>
    </tr>
    <tr>
      <th>27</th>
      <td>20</td>
      <td>4</td>
      <td>23</td>
      <td>25</td>
      <td>15</td>
      <td>-122.408432</td>
      <td>37.788777</td>
    </tr>
    <tr>
      <th>28</th>
      <td>18</td>
      <td>7</td>
      <td>16</td>
      <td>31</td>
      <td>1</td>
      <td>-122.403031</td>
      <td>37.787023</td>
    </tr>
    <tr>
      <th>29</th>
      <td>16</td>
      <td>9</td>
      <td>20</td>
      <td>26</td>
      <td>15</td>
      <td>-122.427880</td>
      <td>37.742015</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>915309</th>
      <td>1</td>
      <td>2</td>
      <td>8</td>
      <td>31</td>
      <td>15</td>
      <td>-122.397208</td>
      <td>37.775333</td>
    </tr>
    <tr>
      <th>915310</th>
      <td>36</td>
      <td>2</td>
      <td>20</td>
      <td>32</td>
      <td>15</td>
      <td>-122.491605</td>
      <td>37.762979</td>
    </tr>
    <tr>
      <th>915311</th>
      <td>34</td>
      <td>8</td>
      <td>10</td>
      <td>32</td>
      <td>0</td>
      <td>-122.461583</td>
      <td>37.745653</td>
    </tr>
    <tr>
      <th>915312</th>
      <td>1</td>
      <td>9</td>
      <td>15</td>
      <td>31</td>
      <td>15</td>
      <td>-122.399981</td>
      <td>37.777624</td>
    </tr>
    <tr>
      <th>915313</th>
      <td>1</td>
      <td>4</td>
      <td>3</td>
      <td>33</td>
      <td>15</td>
      <td>-122.413609</td>
      <td>37.784697</td>
    </tr>
    <tr>
      <th>915314</th>
      <td>1</td>
      <td>2</td>
      <td>21</td>
      <td>29</td>
      <td>15</td>
      <td>-122.453982</td>
      <td>37.771428</td>
    </tr>
    <tr>
      <th>915315</th>
      <td>20</td>
      <td>2</td>
      <td>8</td>
      <td>25</td>
      <td>15</td>
      <td>-122.401857</td>
      <td>37.796626</td>
    </tr>
    <tr>
      <th>915316</th>
      <td>16</td>
      <td>9</td>
      <td>20</td>
      <td>25</td>
      <td>15</td>
      <td>-122.412269</td>
      <td>37.790673</td>
    </tr>
    <tr>
      <th>915317</th>
      <td>16</td>
      <td>2</td>
      <td>10</td>
      <td>25</td>
      <td>15</td>
      <td>-122.406659</td>
      <td>37.788275</td>
    </tr>
    <tr>
      <th>915318</th>
      <td>20</td>
      <td>8</td>
      <td>14</td>
      <td>29</td>
      <td>15</td>
      <td>-122.447689</td>
      <td>37.773732</td>
    </tr>
    <tr>
      <th>915319</th>
      <td>20</td>
      <td>2</td>
      <td>12</td>
      <td>25</td>
      <td>15</td>
      <td>-122.410691</td>
      <td>37.807891</td>
    </tr>
    <tr>
      <th>915320</th>
      <td>20</td>
      <td>2</td>
      <td>18</td>
      <td>31</td>
      <td>15</td>
      <td>-122.406842</td>
      <td>37.775871</td>
    </tr>
    <tr>
      <th>915321</th>
      <td>35</td>
      <td>7</td>
      <td>2</td>
      <td>25</td>
      <td>15</td>
      <td>-122.407152</td>
      <td>37.790366</td>
    </tr>
    <tr>
      <th>915322</th>
      <td>20</td>
      <td>7</td>
      <td>2</td>
      <td>29</td>
      <td>15</td>
      <td>-122.448578</td>
      <td>37.769798</td>
    </tr>
    <tr>
      <th>915323</th>
      <td>16</td>
      <td>2</td>
      <td>14</td>
      <td>25</td>
      <td>15</td>
      <td>-122.412069</td>
      <td>37.799706</td>
    </tr>
    <tr>
      <th>915324</th>
      <td>20</td>
      <td>4</td>
      <td>13</td>
      <td>31</td>
      <td>15</td>
      <td>-122.408068</td>
      <td>37.783992</td>
    </tr>
    <tr>
      <th>915325</th>
      <td>21</td>
      <td>2</td>
      <td>14</td>
      <td>31</td>
      <td>15</td>
      <td>-122.403405</td>
      <td>37.775421</td>
    </tr>
    <tr>
      <th>915326</th>
      <td>37</td>
      <td>8</td>
      <td>23</td>
      <td>32</td>
      <td>0</td>
      <td>-122.478885</td>
      <td>37.725844</td>
    </tr>
    <tr>
      <th>915327</th>
      <td>7</td>
      <td>2</td>
      <td>15</td>
      <td>32</td>
      <td>0</td>
      <td>-122.475306</td>
      <td>37.723336</td>
    </tr>
    <tr>
      <th>915328</th>
      <td>7</td>
      <td>2</td>
      <td>15</td>
      <td>32</td>
      <td>0</td>
      <td>-122.475306</td>
      <td>37.723336</td>
    </tr>
    <tr>
      <th>915329</th>
      <td>37</td>
      <td>2</td>
      <td>15</td>
      <td>32</td>
      <td>0</td>
      <td>-122.475306</td>
      <td>37.723336</td>
    </tr>
    <tr>
      <th>915330</th>
      <td>0</td>
      <td>2</td>
      <td>5</td>
      <td>27</td>
      <td>15</td>
      <td>-122.417730</td>
      <td>37.750674</td>
    </tr>
    <tr>
      <th>915331</th>
      <td>1</td>
      <td>8</td>
      <td>16</td>
      <td>27</td>
      <td>15</td>
      <td>-122.420666</td>
      <td>37.752104</td>
    </tr>
    <tr>
      <th>915332</th>
      <td>1</td>
      <td>10</td>
      <td>18</td>
      <td>31</td>
      <td>15</td>
      <td>-122.419184</td>
      <td>37.773414</td>
    </tr>
    <tr>
      <th>915333</th>
      <td>1</td>
      <td>2</td>
      <td>15</td>
      <td>29</td>
      <td>15</td>
      <td>-122.448043</td>
      <td>37.782371</td>
    </tr>
    <tr>
      <th>915334</th>
      <td>1</td>
      <td>10</td>
      <td>10</td>
      <td>33</td>
      <td>15</td>
      <td>-122.415695</td>
      <td>37.782585</td>
    </tr>
    <tr>
      <th>915335</th>
      <td>1</td>
      <td>2</td>
      <td>10</td>
      <td>27</td>
      <td>15</td>
      <td>-122.410478</td>
      <td>37.766246</td>
    </tr>
    <tr>
      <th>915336</th>
      <td>1</td>
      <td>11</td>
      <td>0</td>
      <td>31</td>
      <td>15</td>
      <td>-122.404270</td>
      <td>37.784479</td>
    </tr>
    <tr>
      <th>915337</th>
      <td>36</td>
      <td>2</td>
      <td>20</td>
      <td>29</td>
      <td>15</td>
      <td>-122.440483</td>
      <td>37.775553</td>
    </tr>
    <tr>
      <th>915338</th>
      <td>1</td>
      <td>4</td>
      <td>12</td>
      <td>33</td>
      <td>15</td>
      <td>-122.413238</td>
      <td>37.782843</td>
    </tr>
  </tbody>
</table>
<p>910708 rows × 7 columns</p>
</div>



## Dividimos nuestro conjunto de datos en train y test (80-20)


```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
```


```python
x = ndataset.drop('category',axis=1)
y = ndataset['category']
```


```python
from sklearn import preprocessing
normalized_x = preprocessing.normalize(x)
```


```python
from sklearn.model_selection import train_test_split
x_training, x_test, y_training, y_test = train_test_split(x, y, test_size=0.2)
```


```python
scaler.fit(x_training)
```




    StandardScaler(copy=True, with_mean=True, with_std=True)




```python
x_training.shape
```




    (728566, 6)




```python
y_training.shape
```




    (728566,)




```python
x_test.shape
```




    (182142, 6)




```python
y_test.shape
```




    (182142,)




```python
x_training.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>dayofweek</th>
      <th>hour</th>
      <th>district</th>
      <th>resolution</th>
      <th>latitude</th>
      <th>longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>883397</th>
      <td>4</td>
      <td>15</td>
      <td>26</td>
      <td>15</td>
      <td>-122.440007</td>
      <td>37.721805</td>
    </tr>
    <tr>
      <th>659255</th>
      <td>7</td>
      <td>20</td>
      <td>32</td>
      <td>10</td>
      <td>-122.456086</td>
      <td>37.716630</td>
    </tr>
    <tr>
      <th>135877</th>
      <td>4</td>
      <td>9</td>
      <td>31</td>
      <td>1</td>
      <td>-122.401817</td>
      <td>37.788441</td>
    </tr>
    <tr>
      <th>705598</th>
      <td>7</td>
      <td>11</td>
      <td>32</td>
      <td>15</td>
      <td>-122.481183</td>
      <td>37.743727</td>
    </tr>
    <tr>
      <th>801842</th>
      <td>2</td>
      <td>9</td>
      <td>30</td>
      <td>15</td>
      <td>-122.498185</td>
      <td>37.780583</td>
    </tr>
  </tbody>
</table>
</div>




```python
x_test.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>dayofweek</th>
      <th>hour</th>
      <th>district</th>
      <th>resolution</th>
      <th>latitude</th>
      <th>longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>365170</th>
      <td>9</td>
      <td>11</td>
      <td>27</td>
      <td>15</td>
      <td>-122.416726</td>
      <td>37.757954</td>
    </tr>
    <tr>
      <th>625791</th>
      <td>8</td>
      <td>18</td>
      <td>25</td>
      <td>15</td>
      <td>-122.412453</td>
      <td>37.798066</td>
    </tr>
    <tr>
      <th>459490</th>
      <td>2</td>
      <td>19</td>
      <td>31</td>
      <td>15</td>
      <td>-122.410406</td>
      <td>37.778784</td>
    </tr>
    <tr>
      <th>225368</th>
      <td>7</td>
      <td>8</td>
      <td>24</td>
      <td>15</td>
      <td>-122.397121</td>
      <td>37.737121</td>
    </tr>
    <tr>
      <th>533255</th>
      <td>9</td>
      <td>9</td>
      <td>31</td>
      <td>15</td>
      <td>-122.403405</td>
      <td>37.775421</td>
    </tr>
  </tbody>
</table>
</div>




```python
y_training.head(5)
```




    883397    16
    659255    27
    135877    34
    705598    16
    801842    20
    Name: category, dtype: int8




```python
y_test.head(5)
```




    365170    16
    625791    16
    459490    36
    225368    20
    533255    16
    Name: category, dtype: int8




```python
incidents.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>category</th>
      <th>type</th>
      <th>dayofweek</th>
      <th>date</th>
      <th>time</th>
      <th>day</th>
      <th>year</th>
      <th>month</th>
      <th>hour</th>
      <th>district</th>
      <th>resolution</th>
      <th>latitude</th>
      <th>longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>VANDALISM</td>
      <td>MALICIOUS MISCHIEF</td>
      <td>Monday</td>
      <td>2007-10-22</td>
      <td>14:30:00</td>
      <td>22</td>
      <td>2007</td>
      <td>10</td>
      <td>14</td>
      <td>TARAVAL</td>
      <td>NONE</td>
      <td>-122.466758005159</td>
      <td>37.729185</td>
    </tr>
    <tr>
      <th>1</th>
      <td>OTHER OFFENSES</td>
      <td>RESISTING ARREST</td>
      <td>Sunday</td>
      <td>2008-03-02</td>
      <td>21:31:00</td>
      <td>02</td>
      <td>2008</td>
      <td>3</td>
      <td>21</td>
      <td>TENDERLOIN</td>
      <td>ARREST, BOOKED</td>
      <td>-122.412224164736</td>
      <td>37.782073</td>
    </tr>
    <tr>
      <th>2</th>
      <td>VANDALISM</td>
      <td>MALICIOUS MISCHIEF, VANDALISM OF VEHICLES</td>
      <td>Friday</td>
      <td>2009-10-30</td>
      <td>19:30:00</td>
      <td>30</td>
      <td>2009</td>
      <td>10</td>
      <td>19</td>
      <td>NORTHERN</td>
      <td>NONE</td>
      <td>-122.422253466945</td>
      <td>37.790863</td>
    </tr>
    <tr>
      <th>3</th>
      <td>OTHER OFFENSES</td>
      <td>PROBATION VIOLATION</td>
      <td>Wednesday</td>
      <td>2011-01-19</td>
      <td>16:25:00</td>
      <td>19</td>
      <td>2011</td>
      <td>1</td>
      <td>16</td>
      <td>INGLESIDE</td>
      <td>ARREST, BOOKED</td>
      <td>-122.447125045686</td>
      <td>37.721031</td>
    </tr>
    <tr>
      <th>4</th>
      <td>NON-CRIMINAL</td>
      <td>AIDED CASE, MENTAL DISTURBED</td>
      <td>Friday</td>
      <td>2008-09-12</td>
      <td>13:21:00</td>
      <td>12</td>
      <td>2008</td>
      <td>9</td>
      <td>13</td>
      <td>MISSION</td>
      <td>PSYCHOPATHIC CASE</td>
      <td>-122.416954468807</td>
      <td>37.753880</td>
    </tr>
  </tbody>
</table>
</div>



Aplicamos las transformaciones una vez realizada la normalización de los datos


```python
x_training = scaler.transform(x_training)
x_test = scaler.transform(x_test)

x_training
x_test
```




    array([[ 0.57387139, -0.37478645, -0.49875567,  0.61102238,  0.22123375,
            -0.03391293],
           [ 0.24573886,  0.69989466, -1.20854942,  0.61102238,  0.36767567,
             0.0736289 ],
           [-1.72305628,  0.85342053,  0.92083182,  0.61102238,  0.43782599,
             0.02193366],
           ...,
           [ 0.90200391, -1.75651931,  1.63062557,  0.61102238,  0.37550202,
             0.03075116],
           [ 0.90200391, -0.83536407, -0.49875567,  0.61102238,  0.29080635,
            -0.02926956],
           [-0.08239366,  0.69989466, -0.49875567,  0.61102238,  0.13615038,
            -0.0278006 ]])



## Usamos un clasificador con el ensemble Random Forest


```python
clf = RandomForestClassifier(max_features="log2", max_depth=11, n_estimators=24,
                             min_samples_split=1000, oob_score=True)
clf
```




    RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
                max_depth=11, max_features='log2', max_leaf_nodes=None,
                min_impurity_decrease=0.0, min_impurity_split=None,
                min_samples_leaf=1, min_samples_split=1000,
                min_weight_fraction_leaf=0.0, n_estimators=24, n_jobs=1,
                oob_score=True, random_state=None, verbose=0, warm_start=False)



## Entrenamos el modelo


```python
clf.fit(x_training,y_training)
```




    RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
                max_depth=11, max_features='log2', max_leaf_nodes=None,
                min_impurity_decrease=0.0, min_impurity_split=None,
                min_samples_leaf=1, min_samples_split=1000,
                min_weight_fraction_leaf=0.0, n_estimators=24, n_jobs=1,
                oob_score=True, random_state=None, verbose=0, warm_start=False)




```python
print("Training set score: %f" % clf.score(x_training, y_training))
print("Test set score: %f" % clf.score(x_test, y_test))
```

    Training set score: 0.362146
    Test set score: 0.359434
    

## Predicciones y Evaluación
Ahora que tenemos un modelo, es hora de usarlo para obtener predicciones 


```python
predictions = clf.predict(x_test)
predictions
```




    array([16, 16, 16, ..., 16, 16, 16], dtype=int8)



Ahora podemos usar las métricas integradas de SciKit-Learn, como un informe de clasificación y una matriz de confusión para evaluar el rendimiento de nuestro modelo:


```python
from sklearn.metrics import classification_report,confusion_matrix
m = confusion_matrix(y_test,predictions)
m.size
```




    1521




```python
print(classification_report(y_test,predictions))
```

                 precision    recall  f1-score   support
    
              0       0.00      0.00      0.00       339
              1       0.20      0.05      0.08     15987
              2       0.00      0.00      0.00        66
              3       0.00      0.00      0.00        68
              4       0.00      0.00      0.00      7416
              5       0.00      0.00      0.00       747
              6       0.00      0.00      0.00       435
              7       0.38      0.38      0.38      8504
              8       0.00      0.00      0.00       696
              9       0.00      0.00      0.00       225
             10       0.00      0.00      0.00        73
             11       0.00      0.00      0.00        78
             12       0.33      0.01      0.02      1642
             13       0.32      0.00      0.00      3386
             14       0.00      0.00      0.00        31
             15       0.00      0.00      0.00       374
             16       0.36      0.94      0.52     44670
             17       0.00      0.00      0.00       291
             18       0.00      0.00      0.00       162
             19       0.84      0.39      0.54      5249
             20       0.47      0.14      0.21     19576
             21       0.33      0.58      0.42     24381
             22       0.00      0.00      0.00         5
             23       0.81      0.23      0.35      1135
             24       0.00      0.00      0.00        55
             25       0.00      0.00      0.00      4421
             26       0.00      0.00      0.00       329
             27       0.00      0.00      0.00      2214
             28       0.00      0.00      0.00      1008
             29       0.00      0.00      0.00        41
             30       0.00      0.00      0.00       937
             31       0.00      0.00      0.00        84
             32       0.00      0.00      0.00      6755
             33       0.00      0.00      0.00         1
             34       0.00      0.00      0.00      1708
             35       0.36      0.00      0.00     10061
             36       0.24      0.02      0.04      9431
             37       0.39      0.02      0.04      7680
             38       0.00      0.00      0.00      1881
    
    avg / total       0.30      0.36      0.25    182142
    
    

## Otra forma de calcular el accuracy


```python
from sklearn.metrics import accuracy_score
```


```python
accuracy_score(y_test, predictions)
```




    0.35943384831614894



# Probaremos con varios modelos adicionales


```python
scoring = 'accuracy'
```


```python
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))
```


```python
results = []
names = []
seed = 7
```


```python
for name, model in models:
    kfold = model_selection.KFold(n_splits=10, random_state=seed)
    cv_results = model_selection.cross_val_score(model, x_training, y_training, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)
```

    LR: 0.321792 (0.001520)
    LDA: 0.320461 (0.001383)
    KNN: 0.296550 (0.000955)
    CART: 0.294909 (0.001151)
    NB: 0.142842 (0.023756)
    


```python
fig = plt.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()
```


```python
knn = KNeighborsClassifier()
knn.fit(x_training, y_training)
predictions = knn.predict(x_test)
```


```python
svm = SVC()
svm.fit(x_training, y_training)
predictions = svm.predict(y_test)
```
