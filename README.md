# zerofile
A filehost focused on being simple to use and lightweight, using no libraries or frameworks.
Uses Django/Python for backend.

## Installation
This only depends on django and python-magic. To install them with pip, do:

```bash
pip3 install Django==2.2.17 python-magic 
```


Additionally, you'll have to create two files in django's BASE_DIR:
- key: Put your SECRET_KEY in here. If this is missing, a dev env will be assumed and a default key be used.
- database: Put your django DATABASE settings in here (in JSON).  
