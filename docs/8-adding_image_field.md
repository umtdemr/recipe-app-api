# Imagefield eklemek

Pillow a gerek var. Pillow da belli linux paketlerine ihtiyaç duyar buna göre requirements.txt a pillow ekleyip dockerfile a da pillow requirementlarını yazmamız gerekir.

```dockerfile
# jpeg dev muslt dev zlib zlib dev ekle

RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps
RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/web/media  # -p eğer yoksa oluştur
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol  -R : sub directory lara da permission ver
RUN chmod -R 755 /vol/web
USER user
```

daha sonra static ve media url root settingsden oluşturulur. urls py da media url ve rootu eklenir


## Imagefield eklemek

### Test işlemi

```py
    from unittest.mock import patch
    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
```

### Model düzeltmesi

```py
import uuid
import os

def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image"""    
    ext = filename.split(".")[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/recipe/', filename)

# added to recipe model: 

image = models.ImageField(null=True, upload_to=recipe_image_file_path)
```