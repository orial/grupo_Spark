
# Análisis de datos con Python y MongoDB

La información del dataset proporcionada por el departamento Policial de San Francisco, se encuentra abierta al público y contiene datos de todas las incidencias generadas por actividades criminales producidas desde el año 2003 hasta la actualidad. Usaremos la base de datos datascience que hemos creado en MongoDB con la coleccion incidents.


```python
%config IPCompleter.greedy=True
```


```python
%matplotlib inline
%config InlineBackend.figure_format='svg'
from IPython.display import display,HTML
import pandas as pd
import seaborn as sns
from scipy.stats import kendalltau
import numpy as np
import math
import matplotlib.pyplot as plt

from prettypandas import PrettyPandas
sns.set(style="ticks")
sns.set_context(context="notebook",font_scale=1)

import string
import tqdm # a cool progress bar
import re
import json

import pymongo
from pymongo import MongoClient
```


```python
########################################################### Database Connection and Load ############################
print('Mongo version', pymongo.__version__)
client = MongoClient('localhost', 27017)
db = client.datascience
collection = db.incidents
```

    Mongo version 3.4.0
    

Calculamos cuantos documentos tenemos en la coleccion


```python
d = db.incidents.count()
d
```




    2186988




```python
#Check if you can access the data from the MongoDB.
cursor = collection.find().sort('sex',pymongo.ASCENDING).limit(1)
for doc in cursor:
    print(doc)
```

    {'_id': ObjectId('5ac48f27a2eb3a9495192d44'), 'IncidntNum': 150060275, 'Category': 'NON-CRIMINAL', 'Descript': 'LOST PROPERTY', 'DayOfWeek': 'Monday', 'Date': '01/19/2015', 'Time': '14:00', 'PdDistrict': 'MISSION', 'Resolution': 'NONE', 'Address': '18TH ST / VALENCIA ST', 'X': -122.42158168137, 'Y': 37.7617007179518, 'Location': '(37.7617007179518, -122.42158168137)', 'PdId': 15006027571000}
    


```python
pipeline = [
        {"$match": {"Category":"ROBBERY"}},
]

aggResult = collection.aggregate(pipeline)
robbery = pd.DataFrame(list(aggResult))
robbery.head()
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
      <th>Address</th>
      <th>Category</th>
      <th>Date</th>
      <th>DayOfWeek</th>
      <th>Descript</th>
      <th>IncidntNum</th>
      <th>Location</th>
      <th>PdDistrict</th>
      <th>PdId</th>
      <th>Resolution</th>
      <th>Time</th>
      <th>X</th>
      <th>Y</th>
      <th>_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>300 Block of LEAVENWORTH ST</td>
      <td>ROBBERY</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>ROBBERY, BODILY FORCE</td>
      <td>150098210</td>
      <td>(37.7841907151119, -122.414406029855)</td>
      <td>TENDERLOIN</td>
      <td>15009821003074</td>
      <td>NONE</td>
      <td>15:45</td>
      <td>-122.414406</td>
      <td>37.784191</td>
      <td>5ac48f27a2eb3a9495192d45</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2200 Block of MARKET ST</td>
      <td>ROBBERY</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>ROBBERY, ARMED WITH A KNIFE</td>
      <td>150098367</td>
      <td>(37.7651107322703, -122.432198022433)</td>
      <td>MISSION</td>
      <td>15009836703072</td>
      <td>NONE</td>
      <td>16:20</td>
      <td>-122.432198</td>
      <td>37.765111</td>
      <td>5ac48f27a2eb3a9495192d52</td>
    </tr>
    <tr>
      <th>2</th>
      <td>PACIFIC AV / GRANT AV</td>
      <td>ROBBERY</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>ROBBERY ON THE STREET, STRONGARM</td>
      <td>150098414</td>
      <td>(37.7969028838908, -122.406831986427)</td>
      <td>CENTRAL</td>
      <td>15009841403014</td>
      <td>ARREST, BOOKED</td>
      <td>17:05</td>
      <td>-122.406832</td>
      <td>37.796903</td>
      <td>5ac48f27a2eb3a9495192d58</td>
    </tr>
    <tr>
      <th>3</th>
      <td>PACIFIC AV / GRANT AV</td>
      <td>ROBBERY</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>ROBBERY, BODILY FORCE</td>
      <td>150098414</td>
      <td>(37.7969028838908, -122.406831986427)</td>
      <td>CENTRAL</td>
      <td>15009841403074</td>
      <td>ARREST, BOOKED</td>
      <td>17:05</td>
      <td>-122.406832</td>
      <td>37.796903</td>
      <td>5ac48f27a2eb3a9495192d59</td>
    </tr>
    <tr>
      <th>4</th>
      <td>400 Block of ELLIS ST</td>
      <td>ROBBERY</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>ATTEMPTED ROBBERY WITH A DEADLY WEAPON</td>
      <td>150098420</td>
      <td>(37.784696907904, -122.413609328985)</td>
      <td>TENDERLOIN</td>
      <td>15009842003473</td>
      <td>ARREST, BOOKED</td>
      <td>17:10</td>
      <td>-122.413609</td>
      <td>37.784697</td>
      <td>5ac48f27a2eb3a9495192d5d</td>
    </tr>
  </tbody>
</table>
</div>




```python
pipeline = [
        {"$match": {"Category":"ASSAULT"}},
]

aggResult = collection.aggregate(pipeline)
assault = pd.DataFrame(list(aggResult))
assault.head()
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
      <th>Address</th>
      <th>Category</th>
      <th>Date</th>
      <th>DayOfWeek</th>
      <th>Descript</th>
      <th>IncidntNum</th>
      <th>Location</th>
      <th>PdDistrict</th>
      <th>PdId</th>
      <th>Resolution</th>
      <th>Time</th>
      <th>X</th>
      <th>Y</th>
      <th>_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>300 Block of LEAVENWORTH ST</td>
      <td>ASSAULT</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>AGGRAVATED ASSAULT WITH BODILY FORCE</td>
      <td>150098210</td>
      <td>(37.7841907151119, -122.414406029855)</td>
      <td>TENDERLOIN</td>
      <td>15009821004014</td>
      <td>NONE</td>
      <td>15:45</td>
      <td>-122.414406</td>
      <td>37.784191</td>
      <td>5ac48f27a2eb3a9495192d46</td>
    </tr>
    <tr>
      <th>1</th>
      <td>PACIFIC AV / GRANT AV</td>
      <td>ASSAULT</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>AGGRAVATED ASSAULT WITH BODILY FORCE</td>
      <td>150098414</td>
      <td>(37.7969028838908, -122.406831986427)</td>
      <td>CENTRAL</td>
      <td>15009841404014</td>
      <td>ARREST, BOOKED</td>
      <td>17:05</td>
      <td>-122.406832</td>
      <td>37.796903</td>
      <td>5ac48f27a2eb3a9495192d5b</td>
    </tr>
    <tr>
      <th>2</th>
      <td>PACIFIC AV / GRANT AV</td>
      <td>ASSAULT</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>BATTERY WITH SERIOUS INJURIES</td>
      <td>150098414</td>
      <td>(37.7969028838908, -122.406831986427)</td>
      <td>CENTRAL</td>
      <td>15009841404136</td>
      <td>ARREST, BOOKED</td>
      <td>17:05</td>
      <td>-122.406832</td>
      <td>37.796903</td>
      <td>5ac48f27a2eb3a9495192d5c</td>
    </tr>
    <tr>
      <th>3</th>
      <td>400 Block of ELLIS ST</td>
      <td>ASSAULT</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>AGGRAVATED ASSAULT WITH BODILY FORCE</td>
      <td>150098420</td>
      <td>(37.784696907904, -122.413609328985)</td>
      <td>TENDERLOIN</td>
      <td>15009842004014</td>
      <td>ARREST, BOOKED</td>
      <td>17:10</td>
      <td>-122.413609</td>
      <td>37.784697</td>
      <td>5ac48f27a2eb3a9495192d5e</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2000 Block of MISSION ST</td>
      <td>ASSAULT</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>BATTERY OF A POLICE OFFICER</td>
      <td>150098458</td>
      <td>(37.764228935718, -122.419520367886)</td>
      <td>MISSION</td>
      <td>15009845804154</td>
      <td>ARREST, BOOKED</td>
      <td>16:56</td>
      <td>-122.419520</td>
      <td>37.764229</td>
      <td>5ac48f27a2eb3a9495192d62</td>
    </tr>
  </tbody>
</table>
</div>




```python
pipeline = [
        {"$match": {"Category":"DRUG/NARCOTIC"}},
]

aggResult = collection.aggregate(pipeline)
drug = pd.DataFrame(list(aggResult))
drug.head()
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
      <th>Address</th>
      <th>Category</th>
      <th>Date</th>
      <th>DayOfWeek</th>
      <th>Descript</th>
      <th>IncidntNum</th>
      <th>Location</th>
      <th>PdDistrict</th>
      <th>PdId</th>
      <th>Resolution</th>
      <th>Time</th>
      <th>X</th>
      <th>Y</th>
      <th>_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1700 Block of HARRISON ST</td>
      <td>DRUG/NARCOTIC</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>POSSESSION OF METH-AMPHETAMINE</td>
      <td>150098345</td>
      <td>(37.7690748003847, -122.413354187018)</td>
      <td>MISSION</td>
      <td>15009834516650</td>
      <td>ARREST, BOOKED</td>
      <td>14:00</td>
      <td>-122.413354</td>
      <td>37.769075</td>
      <td>5ac48f27a2eb3a9495192d4f</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1700 Block of HARRISON ST</td>
      <td>DRUG/NARCOTIC</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>POSSESSION OF NARCOTICS PARAPHERNALIA</td>
      <td>150098345</td>
      <td>(37.7690748003847, -122.413354187018)</td>
      <td>MISSION</td>
      <td>15009834516710</td>
      <td>ARREST, BOOKED</td>
      <td>14:00</td>
      <td>-122.413354</td>
      <td>37.769075</td>
      <td>5ac48f27a2eb3a9495192d50</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2000 Block of MISSION ST</td>
      <td>DRUG/NARCOTIC</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>POSSESSION OF BASE/ROCK COCAINE FOR SALE</td>
      <td>150098458</td>
      <td>(37.764228935718, -122.419520367886)</td>
      <td>MISSION</td>
      <td>15009845816623</td>
      <td>ARREST, BOOKED</td>
      <td>16:56</td>
      <td>-122.419520</td>
      <td>37.764229</td>
      <td>5ac48f27a2eb3a9495192d64</td>
    </tr>
    <tr>
      <th>3</th>
      <td>MISSION ST / 15TH ST</td>
      <td>DRUG/NARCOTIC</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>POSSESSION OF METH-AMPHETAMINE</td>
      <td>150098527</td>
      <td>(37.7666737551835, -122.419827929961)</td>
      <td>MISSION</td>
      <td>15009852716650</td>
      <td>ARREST, BOOKED</td>
      <td>17:02</td>
      <td>-122.419828</td>
      <td>37.766674</td>
      <td>5ac48f27a2eb3a9495192d6e</td>
    </tr>
    <tr>
      <th>4</th>
      <td>700 Block of MARKET ST</td>
      <td>DRUG/NARCOTIC</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>POSSESSION OF MARIJUANA</td>
      <td>150098997</td>
      <td>(37.7871160984672, -122.403919148357)</td>
      <td>SOUTHERN</td>
      <td>15009899716010</td>
      <td>NONE</td>
      <td>20:35</td>
      <td>-122.403919</td>
      <td>37.787116</td>
      <td>5ac48f27a2eb3a9495192da7</td>
    </tr>
  </tbody>
</table>
</div>



### Averiguar que tipos de resoluciones existen en nuestros datos


```python
db.incidents.distinct( "Resolution" )
```




    ['NONE',
     'ARREST, BOOKED',
     'EXCEPTIONAL CLEARANCE',
     'ARREST, CITED',
     'UNFOUNDED',
     'JUVENILE BOOKED',
     'CLEARED-CONTACT JUVENILE FOR MORE INFO',
     'PSYCHOPATHIC CASE',
     'LOCATED',
     'JUVENILE ADMONISHED',
     'COMPLAINANT REFUSES TO PROSECUTE',
     'PROSECUTED BY OUTSIDE AGENCY',
     'NOT PROSECUTED',
     'JUVENILE CITED',
     'JUVENILE DIVERTED',
     'DISTRICT ATTORNEY REFUSES TO PROSECUTE',
     'PROSECUTED FOR LESSER OFFENSE']



### Distribucion de Categories


```python
print("{} robberies ({:.1%}), {} assaults ({:.1%}), {} drugs ({:.1%})".format(
    len(robbery),len(robbery)/d,
    len(assault),len(assault)/d,
    len(drug),len(drug)/d))
```

    55242 robberies (2.5%), 191952 assaults (8.8%), 118739 drugs (5.4%)
    


```python
from pprint import pprint
cursor = collection.find().sort('Category',pymongo.ASCENDING).limit(10)
for doc in cursor:
    pprint(doc)
```

    {'Address': 'SACRAMENTO ST / POLK ST',
     'Category': 'ARSON',
     'Date': '01/04/2014',
     'DayOfWeek': 'Saturday',
     'Descript': 'ARSON',
     'IncidntNum': 140009459,
     'Location': '(37.7914943051906, -122.420874632415)',
     'PdDistrict': 'NORTHERN',
     'PdId': 14000945926030,
     'Resolution': 'ARREST, BOOKED',
     'Time': '03:52',
     'X': -122.420874632415,
     'Y': 37.7914943051906,
     '_id': ObjectId('5ac48f27a2eb3a9495192d63')}
    {'Address': '500 Block of VALENCIA ST',
     'Category': 'ARSON',
     'Date': '02/02/2015',
     'DayOfWeek': 'Monday',
     'Descript': 'ARSON OF AN INHABITED DWELLING',
     'IncidntNum': 150100081,
     'Location': '(37.7640888944532, -122.421876488492)',
     'PdDistrict': 'MISSION',
     'PdId': 15010008126036,
     'Resolution': 'ARREST, BOOKED',
     'Time': '10:05',
     'X': -122.421876488492,
     'Y': 37.7640888944532,
     '_id': ObjectId('5ac48f27a2eb3a9495192e25')}
    {'Address': '200 Block of SHOTWELL ST',
     'Category': 'ARSON',
     'Date': '02/02/2015',
     'DayOfWeek': 'Monday',
     'Descript': 'ARSON OF A VEHICLE',
     'IncidntNum': 150100677,
     'Location': '(37.7644225165568, -122.416374835778)',
     'PdDistrict': 'MISSION',
     'PdId': 15010067726031,
     'Resolution': 'NONE',
     'Time': '12:56',
     'X': -122.416374835778,
     'Y': 37.7644225165568,
     '_id': ObjectId('5ac48f27a2eb3a9495192e63')}
    {'Address': '0 Block of REARDON RD',
     'Category': 'ARSON',
     'Date': '02/02/2015',
     'DayOfWeek': 'Monday',
     'Descript': 'ARSON OF A VEHICLE',
     'IncidntNum': 150102162,
     'Location': '(37.7294874636559, -122.376900658814)',
     'PdDistrict': 'BAYVIEW',
     'PdId': 15010216226031,
     'Resolution': 'NONE',
     'Time': '20:30',
     'X': -122.376900658814,
     'Y': 37.7294874636559,
     '_id': ObjectId('5ac48f27a2eb3a9495192f10')}
    {'Address': '0 Block of MIDDLEPOINT RD',
     'Category': 'ARSON',
     'Date': '02/03/2015',
     'DayOfWeek': 'Tuesday',
     'Descript': 'ARSON OF A VEHICLE',
     'IncidntNum': 150102877,
     'Location': '(37.7357419068572, -122.37934537972)',
     'PdDistrict': 'BAYVIEW',
     'PdId': 15010287726031,
     'Resolution': 'NONE',
     'Time': '05:08',
     'X': -122.37934537972,
     'Y': 37.7357419068572,
     '_id': ObjectId('5ac48f27a2eb3a9495192f6f')}
    {'Address': '300 Block of SAWYER ST',
     'Category': 'ARSON',
     'Date': '02/03/2015',
     'DayOfWeek': 'Tuesday',
     'Descript': 'ARSON OF AN INHABITED DWELLING',
     'IncidntNum': 150104209,
     'Location': '(37.7137889657104, -122.414200995694)',
     'PdDistrict': 'INGLESIDE',
     'PdId': 15010420926036,
     'Resolution': 'NONE',
     'Time': '13:15',
     'X': -122.414200995694,
     'Y': 37.7137889657104,
     '_id': ObjectId('5ac48f27a2eb3a9495193007')}
    {'Address': 'INGERSON AV / GRIFFITH ST',
     'Category': 'ARSON',
     'Date': '02/02/2015',
     'DayOfWeek': 'Monday',
     'Descript': 'ARSON OF A VEHICLE',
     'IncidntNum': 150106249,
     'Location': '(37.716962016099, -122.389279211854)',
     'PdDistrict': 'BAYVIEW',
     'PdId': 15010624926031,
     'Resolution': 'NONE',
     'Time': '02:06',
     'X': -122.389279211854,
     'Y': 37.716962016099,
     '_id': ObjectId('5ac48f27a2eb3a94951930fb')}
    {'Address': '700 Block of ROLPH ST',
     'Category': 'ARSON',
     'Date': '02/03/2015',
     'DayOfWeek': 'Tuesday',
     'Descript': 'ARSON OF A VEHICLE',
     'IncidntNum': 150106534,
     'Location': '(37.7117445002313, -122.431015257276)',
     'PdDistrict': 'INGLESIDE',
     'PdId': 15010653426031,
     'Resolution': 'NONE',
     'Time': '18:00',
     'X': -122.431015257276,
     'Y': 37.7117445002313,
     '_id': ObjectId('5ac48f27a2eb3a949519311a')}
    {'Address': 'TEHAMA ST / 1ST ST',
     'Category': 'ARSON',
     'Date': '06/17/2014',
     'DayOfWeek': 'Tuesday',
     'Descript': 'ARSON',
     'IncidntNum': 140504120,
     'Location': '(37.7880925564265, -122.395481217023)',
     'PdDistrict': 'SOUTHERN',
     'PdId': 14050412026030,
     'Resolution': 'NONE',
     'Time': '22:11',
     'X': -122.395481217023,
     'Y': 37.7880925564265,
     '_id': ObjectId('5ac48f27a2eb3a94951933c6')}
    {'Address': '700 Block of BAY ST',
     'Category': 'ARSON',
     'Date': '02/06/2015',
     'DayOfWeek': 'Friday',
     'Descript': 'ARSON',
     'IncidntNum': 150115585,
     'Location': '(37.8048384367685, -122.419359266314)',
     'PdDistrict': 'CENTRAL',
     'PdId': 15011558526030,
     'Resolution': 'NONE',
     'Time': '21:00',
     'X': -122.419359266314,
     'Y': 37.8048384367685,
     '_id': ObjectId('5ac48f27a2eb3a9495193508')}
    


```python
# aislar los dias Sunday
aggResult = collection.aggregate([{"$match": {"DayOfWeek":"Sunday"}}])
sunday = pd.DataFrame(list(aggResult))
```


```python
# aislar los dias Saturday 
aggResult = collection.aggregate([{"$match": {"DayOfWeek":"Saturday"}}])
saturday = pd.DataFrame(list(aggResult))
```


```python
print("{} Domingos ({:.1%}), {} Sabados ({:.1%})".format(
    len(sunday),len(sunday)/d,
    len(saturday),len(saturday)/d))
```

    290936 Domingos (13.3%), 316451 Sabados (14.5%)
    

## Consultas varias

#### Número de incidencias en Sunday


```python
db.incidents.count({"DayOfWeek":"Sunday"})
```




    290936



#### Incidencias en el dia 02/01/2015


```python
pipeline = [
        {"$match": {"Date":"02/01/2015"}},
]

aggResult = collection.aggregate(pipeline)
dia = pd.DataFrame(list(aggResult))
dia.head()
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
      <th>Address</th>
      <th>Category</th>
      <th>Date</th>
      <th>DayOfWeek</th>
      <th>Descript</th>
      <th>IncidntNum</th>
      <th>Location</th>
      <th>PdDistrict</th>
      <th>PdId</th>
      <th>Resolution</th>
      <th>Time</th>
      <th>X</th>
      <th>Y</th>
      <th>_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>300 Block of LEAVENWORTH ST</td>
      <td>ROBBERY</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>ROBBERY, BODILY FORCE</td>
      <td>150098210</td>
      <td>(37.7841907151119, -122.414406029855)</td>
      <td>TENDERLOIN</td>
      <td>15009821003074</td>
      <td>NONE</td>
      <td>15:45</td>
      <td>-122.414406</td>
      <td>37.784191</td>
      <td>5ac48f27a2eb3a9495192d45</td>
    </tr>
    <tr>
      <th>1</th>
      <td>300 Block of LEAVENWORTH ST</td>
      <td>ASSAULT</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>AGGRAVATED ASSAULT WITH BODILY FORCE</td>
      <td>150098210</td>
      <td>(37.7841907151119, -122.414406029855)</td>
      <td>TENDERLOIN</td>
      <td>15009821004014</td>
      <td>NONE</td>
      <td>15:45</td>
      <td>-122.414406</td>
      <td>37.784191</td>
      <td>5ac48f27a2eb3a9495192d46</td>
    </tr>
    <tr>
      <th>2</th>
      <td>300 Block of LEAVENWORTH ST</td>
      <td>SECONDARY CODES</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>DOMESTIC VIOLENCE</td>
      <td>150098210</td>
      <td>(37.7841907151119, -122.414406029855)</td>
      <td>TENDERLOIN</td>
      <td>15009821015200</td>
      <td>NONE</td>
      <td>15:45</td>
      <td>-122.414406</td>
      <td>37.784191</td>
      <td>5ac48f27a2eb3a9495192d47</td>
    </tr>
    <tr>
      <th>3</th>
      <td>400 Block of LOCUST ST</td>
      <td>NON-CRIMINAL</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>AIDED CASE -PROPERTY FOR DESTRUCTION</td>
      <td>150098232</td>
      <td>(37.7870853907529, -122.451781767894)</td>
      <td>RICHMOND</td>
      <td>15009823251041</td>
      <td>NONE</td>
      <td>16:21</td>
      <td>-122.451782</td>
      <td>37.787085</td>
      <td>5ac48f27a2eb3a9495192d49</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1700 Block of HARRISON ST</td>
      <td>LARCENY/THEFT</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>PETTY THEFT SHOPLIFTING</td>
      <td>150098345</td>
      <td>(37.7690748003847, -122.413354187018)</td>
      <td>MISSION</td>
      <td>15009834506362</td>
      <td>ARREST, BOOKED</td>
      <td>14:00</td>
      <td>-122.413354</td>
      <td>37.769075</td>
      <td>5ac48f27a2eb3a9495192d4e</td>
    </tr>
  </tbody>
</table>
</div>



#### Número de incidencias el 02/01/2015


```python
db.incidents.count({"Date":"02/01/2015"})
```




    466



#### Incidencias en la Zona de LEAVENWORTH


```python
pipeline = [
        {'$match': {'Address':{'$regex': 'LEAVENWORTH'}}},
]

aggResult = collection.aggregate(pipeline)
zona = pd.DataFrame(list(aggResult))
zona.head()
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
      <th>Address</th>
      <th>Category</th>
      <th>Date</th>
      <th>DayOfWeek</th>
      <th>Descript</th>
      <th>IncidntNum</th>
      <th>Location</th>
      <th>PdDistrict</th>
      <th>PdId</th>
      <th>Resolution</th>
      <th>Time</th>
      <th>X</th>
      <th>Y</th>
      <th>_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>300 Block of LEAVENWORTH ST</td>
      <td>ROBBERY</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>ROBBERY, BODILY FORCE</td>
      <td>150098210</td>
      <td>(37.7841907151119, -122.414406029855)</td>
      <td>TENDERLOIN</td>
      <td>15009821003074</td>
      <td>NONE</td>
      <td>15:45</td>
      <td>-122.414406</td>
      <td>37.784191</td>
      <td>5ac48f27a2eb3a9495192d45</td>
    </tr>
    <tr>
      <th>1</th>
      <td>300 Block of LEAVENWORTH ST</td>
      <td>ASSAULT</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>AGGRAVATED ASSAULT WITH BODILY FORCE</td>
      <td>150098210</td>
      <td>(37.7841907151119, -122.414406029855)</td>
      <td>TENDERLOIN</td>
      <td>15009821004014</td>
      <td>NONE</td>
      <td>15:45</td>
      <td>-122.414406</td>
      <td>37.784191</td>
      <td>5ac48f27a2eb3a9495192d46</td>
    </tr>
    <tr>
      <th>2</th>
      <td>300 Block of LEAVENWORTH ST</td>
      <td>SECONDARY CODES</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>DOMESTIC VIOLENCE</td>
      <td>150098210</td>
      <td>(37.7841907151119, -122.414406029855)</td>
      <td>TENDERLOIN</td>
      <td>15009821015200</td>
      <td>NONE</td>
      <td>15:45</td>
      <td>-122.414406</td>
      <td>37.784191</td>
      <td>5ac48f27a2eb3a9495192d47</td>
    </tr>
    <tr>
      <th>3</th>
      <td>MCALLISTER ST / LEAVENWORTH ST</td>
      <td>RECOVERED VEHICLE</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>VEHICLE, RECOVERED, AUTO</td>
      <td>150098919</td>
      <td>(37.7809258336852, -122.413679376888)</td>
      <td>TENDERLOIN</td>
      <td>15009891907041</td>
      <td>JUVENILE BOOKED</td>
      <td>19:53</td>
      <td>-122.413679</td>
      <td>37.780926</td>
      <td>5ac48f27a2eb3a9495192d99</td>
    </tr>
    <tr>
      <th>4</th>
      <td>MCALLISTER ST / LEAVENWORTH ST</td>
      <td>OTHER OFFENSES</td>
      <td>02/01/2015</td>
      <td>Sunday</td>
      <td>CONTRIBUTING TO THE DELINQUENCY OF MINOR</td>
      <td>150098919</td>
      <td>(37.7809258336852, -122.413679376888)</td>
      <td>TENDERLOIN</td>
      <td>15009891915030</td>
      <td>JUVENILE BOOKED</td>
      <td>19:53</td>
      <td>-122.413679</td>
      <td>37.780926</td>
      <td>5ac48f27a2eb3a9495192d9a</td>
    </tr>
  </tbody>
</table>
</div>



#### Actividad criminal por tipo de delito, por año/dia (por tipo de delito)


```python
pipeline = [
        {'$match': {'Date':{'$regex': '2013'},'Category':'ROBBERY'}},
]

aggResult = collection.aggregate(pipeline)
act = pd.DataFrame(list(aggResult))
act.head()
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
      <th>Address</th>
      <th>Category</th>
      <th>Date</th>
      <th>DayOfWeek</th>
      <th>Descript</th>
      <th>IncidntNum</th>
      <th>Location</th>
      <th>PdDistrict</th>
      <th>PdId</th>
      <th>Resolution</th>
      <th>Time</th>
      <th>X</th>
      <th>Y</th>
      <th>_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1600 Block of KIRKWOOD AV</td>
      <td>ROBBERY</td>
      <td>02/10/2013</td>
      <td>Sunday</td>
      <td>ROBBERY, ARMED WITH A KNIFE</td>
      <td>130117084</td>
      <td>(37.7386625599684, -122.390952930587)</td>
      <td>BAYVIEW</td>
      <td>13011708403072</td>
      <td>NONE</td>
      <td>01:46</td>
      <td>-122.390953</td>
      <td>37.738663</td>
      <td>5ac48f2fa2eb3a94951ce496</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2200 Block of GEARY BL</td>
      <td>ROBBERY</td>
      <td>09/18/2013</td>
      <td>Wednesday</td>
      <td>ROBBERY, BODILY FORCE</td>
      <td>130790232</td>
      <td>(37.7833242481047, -122.440341074545)</td>
      <td>PARK</td>
      <td>13079023203074</td>
      <td>NONE</td>
      <td>23:00</td>
      <td>-122.440341</td>
      <td>37.783324</td>
      <td>5ac48f2fa2eb3a94951ce73c</td>
    </tr>
    <tr>
      <th>2</th>
      <td>FULTON ST / BAKER ST</td>
      <td>ROBBERY</td>
      <td>02/27/2013</td>
      <td>Wednesday</td>
      <td>ROBBERY ON THE STREET WITH A GUN</td>
      <td>130168366</td>
      <td>(37.7764331716134, -122.441488426414)</td>
      <td>PARK</td>
      <td>13016836603011</td>
      <td>NONE</td>
      <td>02:32</td>
      <td>-122.441488</td>
      <td>37.776433</td>
      <td>5ac48f2fa2eb3a94951ce804</td>
    </tr>
    <tr>
      <th>3</th>
      <td>MARKET ST / CASTRO ST</td>
      <td>ROBBERY</td>
      <td>03/15/2013</td>
      <td>Friday</td>
      <td>ROBBERY, BODILY FORCE</td>
      <td>130215296</td>
      <td>(37.7626702770872, -122.435187699349)</td>
      <td>MISSION</td>
      <td>13021529603074</td>
      <td>NONE</td>
      <td>03:15</td>
      <td>-122.435188</td>
      <td>37.762670</td>
      <td>5ac48f2fa2eb3a94951cea67</td>
    </tr>
    <tr>
      <th>4</th>
      <td>HAYES ST / DIVISADERO ST</td>
      <td>ROBBERY</td>
      <td>09/26/2013</td>
      <td>Thursday</td>
      <td>ATTEMPTED ROBBERY WITH A GUN</td>
      <td>130810830</td>
      <td>(37.7749912944366, -122.437799703468)</td>
      <td>PARK</td>
      <td>13081083003471</td>
      <td>NONE</td>
      <td>07:15</td>
      <td>-122.437800</td>
      <td>37.774991</td>
      <td>5ac48f2fa2eb3a94951ceac5</td>
    </tr>
  </tbody>
</table>
</div>



### Una pequeña función para contar el número de documentos según una colección dada.


```python
def mongo_stats(mg_coll, filter={}):
    try:
        # connect to database
        client = MongoClient('localhost', 27017)
        db = client.datascience
        
        coll = db[mg_coll]
        return coll.find(filter).count()
    except:
        return False
```


```python
mongo_stats("incidents")
```




    2186988



### O una función para obtener el último documento por fecha:


```python
def get_last_doc(mg_coll, filter = {}, query_limit = 1):
    try:
        # connect to database
        client = MongoClient('localhost', 27017)
        db = client.datascience
        
        coll = db[mg_coll]
        cursor = coll.find(filter, limit=query_limit).sort('date',pymongo.ASCENDING)
        return cursor
 
    except Exception as e:
        print ("No se pudo conectar a la base de datos: ", e)
```


```python
from pprint import pprint
for doc in get_last_doc("incidents"):
    pprint(doc)
```

    {'Address': '18TH ST / VALENCIA ST',
     'Category': 'NON-CRIMINAL',
     'Date': '01/19/2015',
     'DayOfWeek': 'Monday',
     'Descript': 'LOST PROPERTY',
     'IncidntNum': 150060275,
     'Location': '(37.7617007179518, -122.42158168137)',
     'PdDistrict': 'MISSION',
     'PdId': 15006027571000,
     'Resolution': 'NONE',
     'Time': '14:00',
     'X': -122.42158168137,
     'Y': 37.7617007179518,
     '_id': ObjectId('5ac48f27a2eb3a9495192d44')}
    
