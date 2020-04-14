# Adding filtering

## test aşaması

bu aşamada 3 adet recipe oluşturup test yapacağız. 2 sine belirli tag veya ingredient eklenecek diğerine eklenmeyecek :)
sonra oluşturulan recipeler serilaizer ile serialize edilip response datasında var mı yok mu kontrol edilecek

```py

def test_filter_recipes_by_tags(self):
    """Test returning recipes with specific tags"""
    recipe1 = sample_recipe(user=self.user, title="Vegatable cherry")
    recipe2 = sample_recipe(user=self.user, title="Thaini obegene")
    tag1 = sample_tag(user=self.user, name='Vegan')
    tag2 = sample_tag(user=self.user, name='Vegatable')
    recipe1.tags.add(tag1)
    recipe2.tags.add(tag2)
    recipe3 = sample_recipe(user=self.user, title='Fish and chips')

    res = self.client.get(
        RECIPES_URL,
        {'tags': f'{tag1.id},{tag2.id}'}
    )

    serializer1 = RecipeSerializer(recipe1)
    serializer2 = RecipeSerializer(recipe2)
    serializer3 = RecipeSerializer(recipe3)
    self.assertIn(serializer1.data, res.data)
    self.assertIn(serializer2.data, res.data)
    self.assertNotIn(serializer3.data, res.data)

def test_filter_recipes_by_ingredients(self):
    """Test returning recipes with specific ingredients"""
    recipe1 = sample_recipe(user=self.user, title="Vegatable cherry")
    recipe2 = sample_recipe(user=self.user, title="Thaini obegene")
    ingredient1 = sample_ingredient(user=self.user, name='Chocolate')
    ingredient2 = sample_ingredient(user=self.user, name='Merhbaaaaa')
    recipe1.ingredients.add(ingredient1)
    recipe2.ingredients.add(ingredient2)
    recipe3 = sample_recipe(user=self.user, title='Mushrooom and stake')

    res = self.client.get(
        RECIPES_URL,
        {'ingredients': f'{ingredient1.id},{ingredient2.id}'}
    )
    serializer1 = RecipeSerializer(recipe1)
    serializer2 = RecipeSerializer(recipe2)
    serializer3 = RecipeSerializer(recipe3)
    self.assertIn(serializer1.data, res.data)
    self.assertIn(serializer2.data, res.data)
    self.assertNotIn(serializer3.data, res.data)
```


## Viewset eklemesi

recipe viewset e bir adet func ekleyelim ve get_queryset func içinde de belli bir filtreleme yapalım

```py

def _params_to_ints(self, qs): # why func starts with _? the reason is its mean private (not in real)
    """Conert a list of string IDs to list of intengers"""
    return [int(str_id) for str_id in qs.split(',')]


def get_queryset(self):
    """Retrieve the recipes for the authenticated user"""
    tags = self.request.query_params.get('tags')
    ingredients = self.request.query_params.get('ingredients')
    queryset = self.queryset 
    if tags:
        tags_ids = self._params_to_ints(tags)
        queryset = queryset.filter(tags__id__in=tags_ids)
    if ingredients:
        ingredients_ids = self._params_to_ints(ingredients)
        queryset = queryset.filter(ingredients__id__in=ingredients_ids)
    return queryset.filter(user=self.request.user)
```


## Asssinged tests

```py

def test_retrieve_tags_assigned_to_recipes(self):
    """Test filtering tags by those assigned to recipes"""
    tag1 = Tag.objects.create(user=self.user, name="Breakfast")
    tag2 = Tag.objects.create(user=self.user, name="Lunch")
    recipe = Recipe.objects.create(
        title="Corona tatlısı",
        time_minutes=2,
        price=5.00,
        user=self.user
    )
    recipe.tags.add(tag1)

    res = self.client.get(TAGS_URL, {"assigned_only": 1})

    serializer1 = TagSerializer(tag1)
    serializer2 = TagSerializer(tag2)
    self.assertIn(serializer1.data, res.data)
    self.assertNotIn(serializer2.data, res.data)

def test_retrieve_tags_assigned_unique(self):
    """Test filtering tags by assigned return unique items"""
    tag = Tag.objects.create(user=self.user, name="Breakfast")
    Tag.objects.create(user=self.user, name="Lunch")
    recipe1 = Recipe.objects.create(
        title="Corona çorbası",
        time_minutes=14,
        price=52.00,
        user=self.user
    )
    recipe1.tags.add(tag)
    recipe2 = Recipe.objects.create(
        title="Coronalı tatlı",
        time_minutes=14,
        price=21.99,
        user=self.user
    )
    recipe2.tags.add(tag)

    res = self.client.get(TAGS_URL, {"assigned_only": 1})

    self.assertEqual(len(res.data), 1)

```

## Viewset tags and ingredients base

```py
def get_queryset(self):
    """Return objects for the current authenticated user"""
    assigned_only = bool(
        int(self.request.query_params.get("assigned_only", 0))
    )
    queryset = self.queryset
    if assigned_only:
        queryset = queryset.filter(recipe__isnull=False)
    return queryset.filter(user=self.request.user).order_by('-name').distinct()


```