# Adding tags

when we can use api test in our custom test we should import APIClient from rest_framework.test. 
Here is a simple example

```py
from django.test import TestCase
from rest_framework.test import APIClient

class SomeTest(TestCase):
    """some test"""

    def setUp(self):
        self.client = APIClient()
        self.client.force_login(user)

```

## Viewset ve APIViews
APIView: This provides methods handler for http verbs: get, post, put, patch, and delete
ViewSets:

* list: read only, returns multiple resources (http verb: get). Returns a list of dicts.
* retrieve: read only, single resource (http verb: get, but will expect an id in the url). Returns a single dict.
* create: creates a new resource (http verb: post)
* update/partial_update: edits a resource (http verbs: put/patch)
* destroy: removes a resource (http verb: delete)

## mixin: from rest_framework import mixins

class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):

> Bu şekilde viewsete mixins verildiğinde diğer otomatik verilmiş mixinler iptal edilir. 


## perform_crate

CreateModelMixin in sahip olduğu yetenek. Kaydedilirken bir relational varsa bunu kullanabiliriz gibime geliyor.