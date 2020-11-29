import factory
from datetime import datetime
from django.contrib.auth.models import User

from . import models


class UsersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user%d' % n)


class ExtendingUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ExtendingUser

    user = factory.SubFactory(UsersFactory)


class BlogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Blog

    user = factory.SubFactory(ExtendingUserFactory)
    created_at = factory.LazyFunction(datetime.now)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Post

    blog = factory.SubFactory(BlogFactory)
    header = factory.Faker('text', max_nb_chars=10)
    text = factory.Faker('text', max_nb_chars=50)
    created_at = factory.LazyFunction(datetime.now)
