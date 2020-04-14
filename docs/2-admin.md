# Admin

## admin test

ilk olarak Client import edilir ki force_login işlemi yapılsın
setUp func içinde login işlemi yapılır
reverse dahil edilir ki admin:core_user_changelist diyip burdan res alalım
assertContains ile bu resi kontrol edelim.

```py
url = reverse('admin:core_user_add')
res = self.client.get(url)

self.assertEqual(res.status_code, 200)  # Bu şekilde istediğimiz sayfanın çalışıp çalışmadığını test edebiliriz.
```