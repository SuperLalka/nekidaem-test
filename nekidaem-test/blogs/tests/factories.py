import factory
from datetime import datetime

from blogs import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Sequence(lambda n: 'user%d' % n)


class BlogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Blog

    author = factory.SubFactory(UserFactory)
    created_at = factory.LazyFunction(datetime.now)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Post

    blog = factory.SubFactory(BlogFactory)
    header = factory.Faker('text', max_nb_chars=10)
    text = factory.Faker('text', max_nb_chars=50)
    created_at = factory.LazyFunction(datetime.now)
