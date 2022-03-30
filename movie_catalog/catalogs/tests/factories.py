import random

import factory


class CatalogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "catalogs.Catalog"

    title = factory.Faker("word")
    description = factory.Faker("sentence")
    is_active = factory.Faker("boolean")
    order = factory.LazyAttribute(lambda x: int(random.randrange(1, 10000)))
