# Progress

## mocking

you can use mocking to avoid sending an actual email

## wait_for_db

Bazen django postgres ile çalışırken hata verebiliyor. Her hata verişinde restart atmamız gerekiyor. wait_for_fb kullanarak bu hatanın önüne geçmiş oluyoruz.

1. create a file in core/test/test_commands.py
2. testleri oluştur
3. core/management/commands içinde wait_for_db commandını oluştur
    > Bunları oluştururken __init__.py lara dikkat et
4. wait_for_db.py:  
```py

import time

from django.db  import connections # test db connection is avilabe
from django.db.utils import OperationalError  # hata çıktısı
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """ django command to pause execution until database is available """

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database is unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
```

5. Docker file django commandını editleyerek wait_for_db ve migrate komutlarını ekleyelim.
```dockerfile
services:
  app:
    build:
        context: .
    command: >
      sh -c "python manage.py wait_for_db &&
             python manage.py migrate &&
             python manage.py runserver 0.0.0.0:8000"
```