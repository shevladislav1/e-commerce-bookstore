# Django E-commerce Bookstore
A simple website built with django
# Installation
clone the repository:

```git clone https://github.com/shevladislav1/e-commerce-bookstore-.git```

create a virtual environment: 

```python -m venv venv```


activate virtual environment:

```venv\Scripts\activate.bat```

installing all dependencies:

```pip install -r requirements.txt```

you will need to set the secret key in .../application/application/settings.py : 

```SECRET_KEY = 'your secret key'```


to get the key you can use the following commands:

```
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
```

### NOTE: 

Also, if you want the system of payment and city selection to work, install api keys:

in settings.py: 
```
LIQPAY_PUBLIC_KEY = 'your LIQPAY_PUBLIC_KEY'
LIQPAY_PRIVATE_KEY = 'your LIQPAY_PRIVATE_KEY'
LIQPAY_SERVER_URL = 'your LIQPAY_SERVER_URL'

API_KEY = 'your API_KEY'
```
for payment:

[Liqpay_api](https://www.liqpay.ua/ru/documentation) 


cities and warehouses:

[novaya_pochta](https://developers.novaposhta.ua/documentation)


# Visuals

![img.png](https://drive.google.com/uc?export=view&id=10cbBUwavMN2WDBU8BYvj3HuCkqYkRnrE)
![img.png](https://drive.google.com/uc?export=view&id=1IsZi5vf4h_8gSnVmGjDQlWXim8sQQiVX)
![img.png](https://drive.google.com/uc?export=view&id=1fAEd3Y7AVZiF_qYdGDc2cXrItsuHc3fe)
![img.png](https://drive.google.com/uc?export=view&id=17ofTHWnUTFCSFF1XJkg0q1kyrpHhrvig)
![img.png](https://drive.google.com/uc?export=view&id=1YHK8rTh16k-_lt5vu5WJKEcStjjN1zNO)
![img.png](https://drive.google.com/uc?export=view&id=1U4Uwg2e9jL-Rqf-ZeCcdP2wcJ0QaZulb)
![img.png](https://drive.google.com/uc?export=view&id=1nC7PeZ0PRiwIoMez4UlVbDZh-YhQ8tvg)
![img.png](https://drive.google.com/uc?export=view&id=1dd2n1xDOQ9mEn-Z5gKGv3H5TGJOx18v6)
![img.png](https://drive.google.com/uc?export=view&id=1ILne5ArviMs9wJJoMv9BXV0V2RnG_IQq)