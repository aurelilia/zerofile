# zerofile
A filehost focused on being simple to use and lightweight, using no libraries or frameworks (except PeerJS when using p2p file streaming).
Uses Django/Python for backend.

## Installation
This only depends on django and python-magic. To install them with pip, do:

```bash
pip3 install Django==3.1.7 python-magic
```

Additionally, you'll have to create two files in django's BASE_DIR:
- key: Put your SECRET_KEY in here. If this is missing, a dev env will be assumed and a default key be used.
- database: Put your django DATABASE settings in here (in JSON).

Lastly, run `compile-sass.sh` to compile SASS into CSS. This uses `sassc`, but you can also
use any other compiler as long as you modify the script accordingly.

## Deploying

[See the Django Documentation on how to deploy.](https://docs.djangoproject.com/en/3.1/howto/deployment/)
