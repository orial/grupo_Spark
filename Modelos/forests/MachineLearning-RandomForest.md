
# Machine Learning - Random Forest


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
print('pandas: {}'.format(pandas.__version__))
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
    pandas: 0.22.0
    sklearn: 0.19.1
    pymongo: 3.4.0
    


```python
import warnings
warnings.filterwarnings('ignore')
```

################################## Load Specific libraries ####################################################


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
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn import preprocessing
from pymongo import MongoClient
```

# Load dataset


```python
client = MongoClient('localhost', 27017)
db = client.datascience
collection = db.incidents
```

## Expand the cursor and construct the DataFrame


```python
cursor = collection.find()
incidents = pd.DataFrame(list(cursor))
```

## Delete the _id



```python
 if no_id:
     del incidents['_id']

 return incidents
```

## Cargaremos un csv de 2018 (menos datos)


```python
incidents = pd.read_csv("Incidents2017.csv")
```

## shape. Dimensions of Dataset


```python
print(incidents.shape)
```

    (154773, 13)
    

## head


```python
print(incidents.head(20))
```

        IncidntNum                Category  \
    0    170670575               EXTORTION   
    1    170670575         SECONDARY CODES   
    2    170644871          OTHER OFFENSES   
    3    170635870          MISSING PERSON   
    4    170616046                 ASSAULT   
    5    170605817      DISORDERLY CONDUCT   
    6    170604449           LARCENY/THEFT   
    7    170591103            NON-CRIMINAL   
    8    170583332          OTHER OFFENSES   
    9    170572868           LARCENY/THEFT   
    10   170572307                 ASSAULT   
    11   170565437                BURGLARY   
    12   170533616                   FRAUD   
    13   170527017  SEX OFFENSES, FORCIBLE   
    14   170514133          SUSPICIOUS OCC   
    15   170465285            NON-CRIMINAL   
    16   170451814            NON-CRIMINAL   
    17   170451109                   FRAUD   
    18   170442158         SECONDARY CODES   
    19   170442158                 ASSAULT   
    
                                                 Descript DayOfWeek        Date  \
    0                                 ATTEMPTED EXTORTION    Sunday  01/01/2017   
    1                                   DOMESTIC VIOLENCE    Sunday  01/01/2017   
    2      FALSE PERSONATION TO RECEIVE MONEY OR PROPERTY    Sunday  01/01/2017   
    3                                       MISSING ADULT    Sunday  01/01/2017   
    4       BATTERY, FORMER SPOUSE OR DATING RELATIONSHIP    Sunday  01/01/2017   
    5                                DISTURBING THE PEACE    Sunday  01/01/2017   
    6   EMBEZZLEMENT FROM DEPENDENT OR ELDER ADULT BY ...    Sunday  01/01/2017   
    7                                       LOST PROPERTY    Sunday  01/01/2017   
    8                                   FALSE PERSONATION    Sunday  01/01/2017   
    9                         GRAND THEFT FROM A BUILDING    Sunday  01/01/2017   
    10                           WILLFUL CRUELTY TO CHILD    Sunday  01/01/2017   
    11                           BURGLARY, FORCIBLE ENTRY    Sunday  01/01/2017   
    12                       CREDIT CARD, THEFT BY USE OF    Sunday  01/01/2017   
    13                                     SEXUAL BATTERY    Sunday  01/01/2017   
    14                              SUSPICIOUS OCCURRENCE    Sunday  01/01/2017   
    15                                     FOUND PROPERTY    Sunday  01/01/2017   
    16                                      LOST PROPERTY    Sunday  01/01/2017   
    17                      FRAUDULENT CREDIT APPLICATION    Sunday  01/01/2017   
    18                                  DOMESTIC VIOLENCE    Sunday  01/01/2017   
    19                        INFLICT INJURY ON COHABITEE    Sunday  01/01/2017   
    
         Time  PdDistrict Resolution                      Address           X  \
    0   00:01    SOUTHERN       NONE        300 Block of SPEAR ST -122.390234   
    1   00:01    SOUTHERN       NONE        300 Block of SPEAR ST -122.390234   
    2   12:00     BAYVIEW       NONE  400 Block of CONNECTICUT ST -122.397378   
    3   08:00    RICHMOND       NONE          400 Block of 6TH AV -122.464280   
    4   10:00     MISSION       NONE        3200 Block of 26TH ST -122.414593   
    5   01:30        PARK       NONE     0 Block of LAKEFOREST CT -122.459893   
    6   00:01    RICHMOND       NONE          500 Block of 2ND AV -122.459722   
    7   12:00     BAYVIEW       NONE   2500 Block of SAN BRUNO AV -122.404407   
    8   00:01     BAYVIEW       NONE   1100 Block of WISCONSIN ST -122.398473   
    9   00:01    SOUTHERN       NONE      300 Block of MISSION ST -122.396211   
    10  00:01        PARK       NONE      1800 Block of WALLER ST -122.454330   
    11  00:01  TENDERLOIN       NONE  200 Block of GOLDEN GATE AV -122.415083   
    12  08:00   INGLESIDE       NONE   3800 Block of SAN BRUNO AV -122.401762   
    13  00:01     MISSION       NONE     100 Block of GUERRERO ST -122.424582   
    14  13:00   INGLESIDE       NONE          0 Block of FOOTE AV -122.445052   
    15  00:01    SOUTHERN       NONE      1200 Block of MARKET ST -122.415449   
    16  00:01    RICHMOND       NONE       5100 Block of GEARY BL -122.474537   
    17  15:00     TARAVAL       NONE        1400 Block of 45TH AV -122.504721   
    18  12:01     BAYVIEW       NONE         1200 Block of 3RD ST -122.389518   
    19  12:01     BAYVIEW       NONE         1200 Block of 3RD ST -122.389518   
    
                Y                                   Location            PdId  
    0   37.789403  (37.789403265990444, -122.39023428729251)  17067057526040  
    1   37.789403  (37.789403265990444, -122.39023428729251)  17067057515200  
    2   37.760588   (37.760588396207226, -122.3973781477237)  17064487109029  
    3   37.780033  (37.780033299100644, -122.46427987944624)  17063587074000  
    4   37.749199    (37.7491990535295, -122.41459317110352)  17061604604138  
    5   37.754792  (37.754791646857264, -122.45989307989882)  17060581719022  
    6   37.778342   (37.77834165784467, -122.45972220947745)  17060444906381  
    7   37.729408   (37.72940755917532, -122.40440718956097)  17059110371000  
    8   37.753148    (37.75314834602312, -122.3984731227604)  17058333209027  
    9   37.790761      (37.790761361966, -122.3962111540381)  17057286806304  
    10  37.768153   (37.76815301111592, -122.45433010539584)  17057230715100  
    11  37.781652  (37.781652445717505, -122.41508317779949)  17056543705071  
    12  37.714524   (37.71452361297482, -122.40176175711419)  17053361609320  
    13  37.768544   (37.76854434073097, -122.42458239880908)  17052701704144  
    14  37.712948   (37.71294771749951, -122.44505165759051)  17051413364070  
    15  37.778294  (37.778293520129026, -122.41544875956173)  17046528572000  
    16  37.780435  (37.780434756690276, -122.47453735746846)  17045181471000  
    17  37.759524   (37.75952426807323, -122.50472074943889)  17045110909340  
    18  37.772468   (37.77246824000607, -122.38951764803554)  17044215815200  
    19  37.772468   (37.77246824000607, -122.38951764803554)  17044215815040  
    

## Statistical summary. descriptions


```python
print(incidents.describe())
```

             IncidntNum              X              Y          PdId
    count  1.547730e+05  154773.000000  154773.000000  1.547730e+05
    mean   1.718220e+08    -122.424253      37.768941  1.718220e+13
    std    4.221544e+06       0.026587       0.023565  4.221544e+11
    min    1.700554e+07    -122.513642      37.707922  1.700554e+12
    25%    1.703404e+08    -122.434308      37.756438  1.703404e+13
    50%    1.706792e+08    -122.417488      37.775421  1.706792e+13
    75%    1.710148e+08    -122.406844      37.785029  1.710148e+13
    max    9.000079e+08    -122.365565      37.819975  9.000079e+13
    

## Class Distribution


```python
print(incidents.groupby('Category').size())
```

    Category
    ARSON                            327
    ASSAULT                        13655
    BAD CHECKS                        24
    BRIBERY                           67
    BURGLARY                        5857
    DISORDERLY CONDUCT               399
    DRIVING UNDER THE INFLUENCE      299
    DRUG/NARCOTIC                   3308
    DRUNKENNESS                      339
    EMBEZZLEMENT                     178
    EXTORTION                         63
    FAMILY OFFENSES                   44
    FORGERY/COUNTERFEITING           509
    FRAUD                           2551
    GAMBLING                          14
    KIDNAPPING                       207
    LARCENY/THEFT                  47826
    LIQUOR LAWS                       77
    LOITERING                         32
    MISSING PERSON                  4487
    NON-CRIMINAL                   17368
    OTHER OFFENSES                 18316
    PORNOGRAPHY/OBSCENE MAT            6
    PROSTITUTION                     527
    RECOVERED VEHICLE                718
    ROBBERY                         3351
    RUNAWAY                          248
    SECONDARY CODES                 2039
    SEX OFFENSES, FORCIBLE          1049
    SEX OFFENSES, NON FORCIBLE        44
    STOLEN PROPERTY                  820
    SUICIDE                           84
    SUSPICIOUS OCC                  6119
    TREA                               1
    TRESPASS                        1613
    VANDALISM                       9765
    VEHICLE THEFT                   5732
    WARRANTS                        5020
    WEAPON LAWS                     1690
    dtype: int64
    

## 1.- Create a Validation Dataset

### We will split the loaded dataset into two, 80% of which we will use to train our models and 20% that we will hold back as a validation dataset.

## Split-out validation dataset


```python
from sklearn.model_selection import train_test_split
train, test = train_test_split(incidents, test_size=0.2)
```


```python
train.shape
```




    (123818, 13)




```python
test.shape
```




    (30955, 13)




```python
weekdays = {'Monday':0., 'Tuesday':1., 'Wednesday':2., 'Thursday': 3., 'Friday':4., 'Saturday':5., 'Sunday':6.}
categories = {c:i for i,c in enumerate(train['Category'].unique())}
cat_rev = {i:c for i,c in enumerate(train['Category'].unique())}
districts = {c:i for i,c in enumerate(train['PdDistrict'].unique())}
dis_rev = {i:c for i,c in enumerate(train['PdDistrict'].unique())}
```

## Extract features from given information


```python
train['Hour'] = list(map(lambda x: float(int(x.split(' ')[0].split(':')[0])),train.Time))
test['Hour'] = list(map(lambda x: float(int(x.split(' ')[0].split(':')[0])),test.Time))

train['Minute'] = list(map(lambda x: float(int(x.split(' ')[0].split(':')[1])),train.Time))
test['Minute'] = list(map(lambda x: float(int(x.split(' ')[0].split(':')[1])),test.Time))

train['Month'] = list(map(lambda x: float(x.split(' ')[0].split('/')[1]), train.Date))
test['Month'] = list(map(lambda x: float(x.split(' ')[0].split('/')[1]), test.Date))

train['Year'] = list(map(lambda x: float(x.split(' ')[0].split('/')[2])-2003., train.Date))
test['Year'] = list(map(lambda x: float(x.split(' ')[0].split('/')[2])-2003., test.Date))

train['Day'] = list(map(lambda x: float(x.split(' ')[0].split('/')[0]), train.Date))
test['Day'] = list(map(lambda x: float(x.split(' ')[0].split('/')[0]), test.Date))

train['Day_Num'] = [float(weekdays[w]) for w in train.DayOfWeek]
test['Day_Num'] = [float(weekdays[w]) for w in test.DayOfWeek]

train['District_Num'] = [float(districts[t]) for t in train.PdDistrict]
test['District_Num'] = [float(districts[t]) for t in test.PdDistrict]

train['Category_Num'] = [float(categories[t]) for t in train.Category]
test['Category_Num'] = [float(categories[t]) for t in test.Category]
```

## Center X,Y coordinates


```python
train['X'] = preprocessing.scale(list(map(lambda x: x+122.4194, train.X)))
train['Y'] = preprocessing.scale(list(map(lambda x: x-37.7749, train.Y)))

test['X'] = preprocessing.scale(list(map(lambda x: x+122.4194, test.X)))
test['Y'] = preprocessing.scale(list(map(lambda x: x-37.7749, test.Y)))
```

## Assign binary value to address by type


```python
def define_address(addr):
    addr_type = 0.
    # Address types:
    #  Intersection: 1
    #  Residence: 0
    if '/' in addr and 'of' not in addr:
        addr_type = 1.
    else:
        add_type = 0.
    return addr_type
```

## Define address feature


```python
train['Address_Num'] = list(map(define_address, train.Address))
test['Address_Num'] = list(map(define_address, test.Address))
```

## Feature selection


```python
X_loc = ['X', 'Y', 'District_Num', 'Address_Num']
X_time = ['Minute', 'Hour']
X_date = ['Year','Month', 'Day', 'Day_Num']
X_all = X_loc + X_time + X_date
```

## Category column we want to predict


```python
y = 'Category_Num'
```


```python
print(train.head())
```

            IncidntNum         Category  \
    84114    170576484    LARCENY/THEFT   
    15060    170103093  SECONDARY CODES   
    11226    176024112        VANDALISM   
    109196   170766124   OTHER OFFENSES   
    134931   170923023         WARRANTS   
    
                                                  Descript  DayOfWeek        Date  \
    84114                     PETTY THEFT FROM LOCKED AUTO   Saturday  07/15/2017   
    15060                                DOMESTIC VIOLENCE     Sunday  02/05/2017   
    11226                    MALICIOUS MISCHIEF, VANDALISM     Friday  01/27/2017   
    109196  FALSE PERSONATION TO RECEIVE MONEY OR PROPERTY  Wednesday  09/13/2017   
    134931                                  WARRANT ARREST     Sunday  11/12/2017   
    
             Time PdDistrict      Resolution                      Address  \
    84114   16:00   NORTHERN            NONE       400 Block of FULTON ST   
    15060   20:42  INGLESIDE  ARREST, BOOKED  1000 Block of VISITACION AV   
    11226   20:00    MISSION            NONE      400 Block of DOLORES ST   
    109196  00:01    MISSION            NONE        3900 Block of 23RD ST   
    134931  14:20   NORTHERN  ARREST, BOOKED        1000 Block of POLK ST   
    
                   X   ...              PdId Month  Year   Day  Day_Num  \
    84114   0.003537   ...    17057648406243  15.0  14.0   7.0      5.0   
    15060   0.562894   ...    17010309315200   5.0  14.0   2.0      6.0   
    11226  -0.077726   ...    17602411228150  27.0  14.0   1.0      4.0   
    109196 -0.250378   ...    17076612409029  13.0  14.0   9.0      2.0   
    134931  0.166122   ...    17092302363010  12.0  14.0  11.0      6.0   
    
            District_Num  Category_Num  Address_Num  Hour  Minute  
    84114            0.0           0.0          0.0  16.0     0.0  
    15060            1.0           1.0          0.0  20.0    42.0  
    11226            2.0           2.0          0.0  20.0     0.0  
    109196           2.0           3.0          0.0   0.0     1.0  
    134931           0.0           4.0          0.0  14.0    20.0  
    
    [5 rows x 22 columns]
    

## Create random forest classifier


```python
clf = RandomForestClassifier(max_features="log2", max_depth=11, n_estimators=24,
                             min_samples_split=1000, oob_score=True)
```

## Fit prediction


```python
clf.fit(train[X_all], train[y])
pred = clf.predict_proba(test[X_all])
```
