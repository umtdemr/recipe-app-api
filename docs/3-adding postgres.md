# Setting up database

> Şifre belirlerken bunun ileride travis gibi araçlarla encrypt edileceğinden emin ol.

depends_on: bağımlılıkları belirtir.

```yml
  app:  # app e db için eklenenler
    environment: 
      - DB_HOST=db
      - DB_NAME=app
      - DB_USER=postgres
      - DB_PASS=supersecretpassword
    depends_on: 
      - db
  
  db:
    image: postgres:10-alpine
    environment: 
      - POSTGRES_DB=app
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=supersecretpassword
```

## Django ile postgres iletişimi

```dockerfile
# docker file for postgres
COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

# İŞLEM BİTTİKTEN SONRA docker-compose build
```


```py
# daha sonra settings.py da düzeltme yapıyoruz:
DATABASES = {
    'default': {
        'ENGINE': 'django.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
    }
}

```