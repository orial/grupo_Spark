
# Neural networks


```python
import sys
import scipy
import numpy
import matplotlib
import pandas
import sklearn
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
```

## Carga del modelo de datos


```python
url = "https://storage.googleapis.com/grupospark/incidents.all.ml.csv"
names = ['category', 'type', 'dayofweek', 'date', 'time','day','year','month','hour','district', 'resolution', 'latitude', 'longitude']
dataset = pandas.read_csv(url, names=names, sep=';')
```

Con ayuda de una red neuronal en Python intentaremos averigüar si dada un distrito y dia de la semana hay posibilidades de producirse un tipo de delito o no. Usaremos el conjunto de datos de incidentes del Repositorio de aprendizaje automático de UCI. Intentaremos construir un modelo que pueda clasificar en función de las situaciones: distrito, dia de la semana  e intentar predecir el tipo de delito que pueda producirse por la zona utilizando redes neuronales.


* Descarte de las columnas para realizar una mejor discretación de los atributos para realizar la clasificación


```python
dataset.drop(dataset.columns[[1,4,5,6,7,8,11,12]], axis=1, inplace=True)
dataset.head
```




    <bound method NDFrame.head of                 category  dayofweek        date    district      resolution
    0           NON-CRIMINAL     Monday  2015-01-19     MISSION            NONE
    1                ROBBERY     Sunday  2015-02-01  TENDERLOIN            NONE
    2                ASSAULT     Sunday  2015-02-01  TENDERLOIN            NONE
    3        SECONDARY CODES     Sunday  2015-02-01  TENDERLOIN            NONE
    4              VANDALISM    Tuesday  2015-01-27    NORTHERN            NONE
    5           NON-CRIMINAL     Sunday  2015-02-01    RICHMOND            NONE
    6        SECONDARY CODES   Saturday  2015-01-31     BAYVIEW            NONE
    7              VANDALISM   Saturday  2015-01-31     BAYVIEW            NONE
    8               BURGLARY   Saturday  2015-01-31     CENTRAL            NONE
    9          LARCENY/THEFT   Saturday  2015-01-31     CENTRAL            NONE
    10         LARCENY/THEFT     Sunday  2015-02-01     MISSION  ARREST, BOOKED
    11         DRUG/NARCOTIC     Sunday  2015-02-01     MISSION  ARREST, BOOKED
    12         DRUG/NARCOTIC     Sunday  2015-02-01     MISSION  ARREST, BOOKED
    13              WARRANTS     Sunday  2015-02-01     MISSION  ARREST, BOOKED
    14               ROBBERY     Sunday  2015-02-01     MISSION            NONE
    15         VEHICLE THEFT     Sunday  2015-02-01    NORTHERN            NONE
    16          NON-CRIMINAL     Sunday  2015-02-01    NORTHERN            NONE
    17              WARRANTS     Sunday  2015-02-01     BAYVIEW  ARREST, BOOKED
    18         LARCENY/THEFT     Sunday  2015-02-01        PARK            NONE
    19        OTHER OFFENSES     Sunday  2015-02-01     BAYVIEW  ARREST, BOOKED
    20               ROBBERY     Sunday  2015-02-01     CENTRAL  ARREST, BOOKED
    21               ROBBERY     Sunday  2015-02-01     CENTRAL  ARREST, BOOKED
    22             VANDALISM     Friday  2016-11-11     MISSION            NONE
    23               ASSAULT     Sunday  2015-02-01     CENTRAL  ARREST, BOOKED
    24               ASSAULT     Sunday  2015-02-01     CENTRAL  ARREST, BOOKED
    25               ROBBERY     Sunday  2015-02-01  TENDERLOIN  ARREST, BOOKED
    26               ASSAULT     Sunday  2015-02-01  TENDERLOIN  ARREST, BOOKED
    27           WEAPON LAWS     Sunday  2015-02-01  TENDERLOIN  ARREST, BOOKED
    28          NON-CRIMINAL     Sunday  2015-02-01     BAYVIEW            NONE
    29        OTHER OFFENSES     Sunday  2015-02-01  TENDERLOIN  ARREST, BOOKED
    ...                  ...        ...         ...         ...             ...
    2214984          ASSAULT     Friday  2017-05-12    SOUTHERN            NONE
    2214985    VEHICLE THEFT     Friday  2017-05-19     TARAVAL            NONE
    2214986         TRESPASS     Sunday  2017-05-21     TARAVAL  ARREST, BOOKED
    2214987          ASSAULT   Thursday  2017-05-18    SOUTHERN            NONE
    2214988          ASSAULT     Monday  2017-05-15  TENDERLOIN            NONE
    2214989          ASSAULT     Friday  2016-12-30        PARK            NONE
    2214990     NON-CRIMINAL     Friday  2016-12-30     CENTRAL            NONE
    2214991    LARCENY/THEFT   Thursday  2016-12-29     CENTRAL            NONE
    2214992    LARCENY/THEFT     Friday  2016-12-30     CENTRAL            NONE
    2214993     NON-CRIMINAL     Sunday  2017-01-08        PARK            NONE
    2214994     NON-CRIMINAL     Friday  2017-01-20     CENTRAL            NONE
    2214995     NON-CRIMINAL     Friday  2017-02-24    SOUTHERN            NONE
    2214996        VANDALISM   Saturday  2017-03-18     CENTRAL            NONE
    2214997     NON-CRIMINAL   Saturday  2017-04-22        PARK            NONE
    2214998    LARCENY/THEFT     Friday  2017-05-05     CENTRAL            NONE
    2214999     NON-CRIMINAL     Monday  2017-05-08    SOUTHERN            NONE
    2215000   OTHER OFFENSES     Friday  2016-12-02    SOUTHERN            NONE
    2215001         WARRANTS     Sunday  2017-05-14     TARAVAL  ARREST, BOOKED
    2215002    DRUG/NARCOTIC     Friday  2017-05-12     TARAVAL  ARREST, BOOKED
    2215003    DRUG/NARCOTIC     Friday  2017-05-12     TARAVAL  ARREST, BOOKED
    2215004         WARRANTS     Friday  2017-05-12     TARAVAL  ARREST, BOOKED
    2215005            ARSON     Friday  2017-01-06     MISSION            NONE
    2215006          ASSAULT     Sunday  2017-01-22     MISSION            NONE
    2215007          ASSAULT    Tuesday  2017-01-31    SOUTHERN            NONE
    2215008          ASSAULT     Friday  2017-02-03        PARK            NONE
    2215009          ASSAULT    Tuesday  2017-02-07  TENDERLOIN            NONE
    2215010          ASSAULT     Friday  2017-02-10     MISSION            NONE
    2215011          ASSAULT  Wednesday  2017-03-01    SOUTHERN            NONE
    2215012    VEHICLE THEFT     Friday  2017-03-03        PARK            NONE
    2215013          ASSAULT     Monday  2017-01-30  TENDERLOIN            NONE
    
    [2215014 rows x 5 columns]>



* Analizamos las columnas elegidas con el fin de analizar la distancia de la importancia entre ellas


```python
dataset.describe().transpose()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>count</th>
      <th>unique</th>
      <th>top</th>
      <th>freq</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>category</th>
      <td>2215014</td>
      <td>39</td>
      <td>LARCENY/THEFT</td>
      <td>480448</td>
    </tr>
    <tr>
      <th>dayofweek</th>
      <td>2215014</td>
      <td>12</td>
      <td>Friday</td>
      <td>336117</td>
    </tr>
    <tr>
      <th>date</th>
      <td>2215014</td>
      <td>5618</td>
      <td>Wednesday</td>
      <td>1989</td>
    </tr>
    <tr>
      <th>district</th>
      <td>2215013</td>
      <td>34</td>
      <td>SOUTHERN</td>
      <td>398432</td>
    </tr>
    <tr>
      <th>resolution</th>
      <td>2215014</td>
      <td>27</td>
      <td>NONE</td>
      <td>1378600</td>
    </tr>
  </tbody>
</table>
</div>



## Normalización de datos
La red neuronal en Python puede tener dificultades para converger antes de la cantidad máxima de iteraciones permitidas si los datos no están normalizados. El Perceptron multicapa es sensible a las incrustaciones de características, por lo que es muy recomendable escalar los datos. Hay que tener en cuenta que debe aplicar la misma escala al conjunto de prueba para obtener resultados significativos. Hay muchos métodos diferentes para la normalización de los datos, utilizaremos el StandardScaler incorporado para la estandarización.


```python
ndataset = dataset
categories = { x: ind for ind, x in enumerate(dataset.category.unique()) }
ndataset['category'] = ndataset['category'].map(lambda x: categories[x])

dayofweek = { x: ind for ind, x in enumerate(dataset.dayofweek.unique()) }
ndataset['dayofweek'] = ndataset['dayofweek'].map(lambda x: dayofweek[x])

district = { x: ind for ind, x in enumerate(dataset.district.unique()) }
ndataset['district'] = ndataset['district'].map(lambda x: district[x])

resolution = { x: ind for ind, x in enumerate(dataset.resolution.unique()) }
ndataset['resolution'] = ndataset['resolution'].map(lambda x: resolution[x])

ndataset.head()

```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>category</th>
      <th>dayofweek</th>
      <th>date</th>
      <th>district</th>
      <th>resolution</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>0</td>
      <td>2015-01-19</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>1</td>
      <td>2015-02-01</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>1</td>
      <td>2015-02-01</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>1</td>
      <td>2015-02-01</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>2</td>
      <td>2015-01-27</td>
      <td>2</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



Normalización de la columna de fecha


```python
import time
import datetime
def totime(x):
    try:
        return time.mktime(datetime.datetime.strptime(x, "%Y-%m-%d").timetuple())
    except ValueError:
        return 0

ndataset['date'] = ndataset['date'].map(totime)

ndataset.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>category</th>
      <th>dayofweek</th>
      <th>date</th>
      <th>district</th>
      <th>resolution</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>0</td>
      <td>1.421622e+09</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>1</td>
      <td>1.422745e+09</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>1</td>
      <td>1.422745e+09</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>1</td>
      <td>1.422745e+09</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>2</td>
      <td>1.422313e+09</td>
      <td>2</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>




```python
ndataset.drop(ndataset.columns[[2]], axis=1, inplace=True)
ndataset.head
```




    <bound method NDFrame.head of          category  dayofweek  district  resolution
    0               0          0         0           0
    1               1          1         1           0
    2               2          1         1           0
    3               3          1         1           0
    4               4          2         2           0
    5               0          1         3           0
    6               3          3         4           0
    7               4          3         4           0
    8               5          3         5           0
    9               6          3         5           0
    10              6          1         0           1
    11              7          1         0           1
    12              7          1         0           1
    13              8          1         0           1
    14              1          1         0           0
    15              9          1         2           0
    16              0          1         2           0
    17              8          1         4           1
    18              6          1         6           0
    19             10          1         4           1
    20              1          1         5           1
    21              1          1         5           1
    22              4          4         0           0
    23              2          1         5           1
    24              2          1         5           1
    25              1          1         1           1
    26              2          1         1           1
    27             11          1         1           1
    28              0          1         4           0
    29             10          1         1           1
    ...           ...        ...       ...         ...
    2214984         2          4         8           0
    2214985         9          4         7           0
    2214986        18          1         7           1
    2214987         2          6         8           0
    2214988         2          0         1           0
    2214989         2          4         6           0
    2214990         0          4         5           0
    2214991         6          6         5           0
    2214992         6          4         5           0
    2214993         0          1         6           0
    2214994         0          4         5           0
    2214995         0          4         8           0
    2214996         4          3         5           0
    2214997         0          3         6           0
    2214998         6          4         5           0
    2214999         0          0         8           0
    2215000        10          4         8           0
    2215001         8          1         7           1
    2215002         7          4         7           1
    2215003         7          4         7           1
    2215004         8          4         7           1
    2215005        12          4         0           0
    2215006         2          1         0           0
    2215007         2          2         8           0
    2215008         2          4         6           0
    2215009         2          2         1           0
    2215010         2          4         0           0
    2215011         2          5         8           0
    2215012         9          4         6           0
    2215013         2          0         1           0
    
    [2215014 rows x 4 columns]>



### División de muestras y entrenamiento.
Dividamos nuestros datos en conjuntos de entrenamiento y prueba, esto se hace fácilmente con la función train_test_split de SciKit Learn de model_selection:


```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
```


```python
x = ndataset.drop('category',axis=1)
y = ndataset['category']
ndataset.head
```




    <bound method NDFrame.head of          category  dayofweek          date  district  resolution
    0               0          0  1.421622e+09         0           0
    1               1          1  1.422745e+09         1           0
    2               2          1  1.422745e+09         1           0
    3               3          1  1.422745e+09         1           0
    4               4          2  1.422313e+09         2           0
    5               0          1  1.422745e+09         3           0
    6               3          3  1.422659e+09         4           0
    7               4          3  1.422659e+09         4           0
    8               5          3  1.422659e+09         5           0
    9               6          3  1.422659e+09         5           0
    10              6          1  1.422745e+09         0           1
    11              7          1  1.422745e+09         0           1
    12              7          1  1.422745e+09         0           1
    13              8          1  1.422745e+09         0           1
    14              1          1  1.422745e+09         0           0
    15              9          1  1.422745e+09         2           0
    16              0          1  1.422745e+09         2           0
    17              8          1  1.422745e+09         4           1
    18              6          1  1.422745e+09         6           0
    19             10          1  1.422745e+09         4           1
    20              1          1  1.422745e+09         5           1
    21              1          1  1.422745e+09         5           1
    22              4          4  1.478819e+09         0           0
    23              2          1  1.422745e+09         5           1
    24              2          1  1.422745e+09         5           1
    25              1          1  1.422745e+09         1           1
    26              2          1  1.422745e+09         1           1
    27             11          1  1.422745e+09         1           1
    28              0          1  1.422745e+09         4           0
    29             10          1  1.422745e+09         1           1
    ...           ...        ...           ...       ...         ...
    2214984         2          4  1.494540e+09         8           0
    2214985         9          4  1.495145e+09         7           0
    2214986        18          1  1.495318e+09         7           1
    2214987         2          6  1.495058e+09         8           0
    2214988         2          0  1.494799e+09         1           0
    2214989         2          4  1.483052e+09         6           0
    2214990         0          4  1.483052e+09         5           0
    2214991         6          6  1.482966e+09         5           0
    2214992         6          4  1.483052e+09         5           0
    2214993         0          1  1.483830e+09         6           0
    2214994         0          4  1.484867e+09         5           0
    2214995         0          4  1.487891e+09         8           0
    2214996         4          3  1.489792e+09         5           0
    2214997         0          3  1.492812e+09         6           0
    2214998         6          4  1.493935e+09         5           0
    2214999         0          0  1.494194e+09         8           0
    2215000        10          4  1.480633e+09         8           0
    2215001         8          1  1.494713e+09         7           1
    2215002         7          4  1.494540e+09         7           1
    2215003         7          4  1.494540e+09         7           1
    2215004         8          4  1.494540e+09         7           1
    2215005        12          4  1.483657e+09         0           0
    2215006         2          1  1.485040e+09         0           0
    2215007         2          2  1.485817e+09         8           0
    2215008         2          4  1.486076e+09         6           0
    2215009         2          2  1.486422e+09         1           0
    2215010         2          4  1.486681e+09         0           0
    2215011         2          5  1.488323e+09         8           0
    2215012         9          4  1.488496e+09         6           0
    2215013         2          0  1.485731e+09         1           0
    
    [2215014 rows x 5 columns]>




```python
x.head(),y.head()
from sklearn.model_selection import train_test_split
x_training, x_test, y_training, y_test = train_test_split(x, y)
```


```python
scaler.fit(x_training)
```




    StandardScaler(copy=True, with_mean=True, with_std=True)



Aplicamos las transformaciones una vez realizada la normalización de los datos


```python
x_training = scaler.transform(x_training)
x_test = scaler.transform(x_test)

x_training
x_test
```




    array([[ 0.96325037,  1.22671595, -1.38651992, -0.35501582],
           [-0.53560579, -1.09092321,  1.03133245, -0.09257125],
           [-1.53484323, -0.08056703,  1.333564  , -0.35501582],
           ..., 
           [-1.53484323,  0.58144307,  0.12463781, -0.35501582],
           [ 0.46363165, -0.30632885,  1.03133245, -0.35501582],
           [ 1.46286909,  0.78584904,  0.12463781,  0.4323179 ]])



## Entrenador del modelo
Ahora es el momento de entrenar a nuestro modelo. SciKit Learn lo hace increíblemente fácil, mediante el uso de objetos estimadores. En este caso, importaremos nuestro estimador (el modelo clasificador de perceptrón multicapa) de la biblioteca neural_network de SciKit-Learn



```python
from sklearn.neural_network import MLPClassifier
```

A continuación, creamos una instancia del modelo, hay muchos parámetros que puede elegir definir y personalizar aquí, solo definiremos hidden_layer_sizes. 

* Para este parámetro, se pasa una tupla que consiste en el número de neuronas que se desea en cada capa, donde la enésima entrada de la tupla representa el número de neuronas en la enésima capa del modelo MLP. 
* Hay muchas maneras de elegir estos números, pero para simplificar, elegiremos 3 capas con el mismo número de neuronas que funciones en nuestro conjunto de datos junto con 100 iteraciones máximas, como ejemplo.


```python
classificador = MLPClassifier(hidden_layer_sizes=(10,10,10), max_iter=500,verbose=10)
classificador
```




    MLPClassifier(activation='relu', alpha=0.0001, batch_size='auto', beta_1=0.9,
           beta_2=0.999, early_stopping=False, epsilon=1e-08,
           hidden_layer_sizes=(10, 10, 10), learning_rate='constant',
           learning_rate_init=0.001, max_iter=500, momentum=0.9,
           nesterovs_momentum=True, power_t=0.5, random_state=None,
           shuffle=True, solver='adam', tol=0.0001, validation_fraction=0.1,
           verbose=10, warm_start=False)




```python
classificador.fit(x_training,y_training)
```

    Iteration 1, loss = 2.33980325
    Iteration 2, loss = 2.26914207
    Iteration 3, loss = 2.25976598


Como podemos ver el resultado muestra los valores predeterminados de los otros parámetros en el modelo. La idea sería ajustar y definir los parámetros de configuración hasta dar con un modelo ajustado a la información a predecir.

## Predicciones y Evaluación
Ahora que tenemos un modelo, es hora de usarlo para obtener predicciones Podemos hacer esto simplemente con el método predict () fuera de nuestro modelo ajustado:


```python
predictions = classificador.predict(x_test)
```

Ahora podemos usar las métricas integradas de SciKit-Learn, como un informe de clasificación y una matriz de confusión para evaluar el rendimiento de nuestro modelo:


```python
from sklearn.metrics import classification_report,confusion_matrix
print(confusion_matrix(y_test,predictions))
```


```python
print(classification_report(y_test,predictions))
```

La desventaja de utilizar un modelo Perceptron multicapa es lo difícil que es interpretar el modelo en sí. Los pesos y los sesgos no serán fácilmente interpretables en relación con qué características son importantes para el modelo en sí.

Sin embargo, si desea extraer los pesos y sesgos MLP después de entrenar su modelo, use sus atributos públicos coefs_ e intercepts_.

coefs_ es una lista de matrices de peso, donde la matriz de ponderación en el índice i representa los pesos entre la capa iy la capa i + 1.

intercepts_ es una lista de vectores de sesgo, donde el vector en el índice i representa los valores de sesgo agregados a la capa i + 1.


```python
len(classificador.coefs_)
```


```python
len(classificador.coefs_[0])
```


```python
len(classificador.intercepts_[0])
```

### Conclusión
Intentaremos jugar con la cantidad de capas y neuronas ocultas y observa cómo afectan los resultados de nuestra red neuronal en Python.
