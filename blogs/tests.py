import factory
from django.db.models import signals
from django.test import TestCase
from hamcrest import *
from rest_framework.test import APIClient

from blogs.factories import (
    UsersFactory,
    ExtendingUserFactory,
    BlogFactory,
    PostFactory
)


class PostsApiTestCase(TestCase):

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def setUp(self):
        self.client = APIClient()

        self.django_user = UsersFactory()
        self.user = ExtendingUserFactory(user=self.django_user)
        self.user_blog = BlogFactory(user=self.user)
        self.user_blog_post = PostFactory(blog=self.user_blog)

        self.client.force_authenticate(user=self.django_user)

    def test_get_post(self):
        response = self.client.get(f'/api/posts/{self.user_blog_post.id}/', follow=True)
        self.assertEqual(response.status_code, 405)

    def test_get_posts_list(self):
        response = self.client.get('/api/posts/', follow=True)
        self.assertEqual(response.status_code, 405)

    def test_create_post(self):
        response = self.client.post('/api/posts/',
                                    {'blog': self.user_blog.id,
                                     'header': 'NEW post header',
                                     'text': 'NEW post text'},
                                    follow=True)
        self.assertEqual(response.status_code, 201)
        assert_that(response.json(), has_entries({
            'header': 'NEW post header',
            'text': 'NEW post text',
        }))

    def test_update_post(self):
        response = self.client.patch(f'/api/posts/{self.user_blog_post.id}/',
                                     {'blog': self.user_blog.id,
                                      'header': 'UPDATE post header',
                                      'text': 'UPDATE post text'},
                                     follow=True)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user_blog_post.header, 'UPDATE post header')

    def test_delete_post(self):
        response = self.client.delete(f'/api/posts/{self.user_blog_post.id}/', follow=True)
        self.assertEqual(response.status_code, 403)
