from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from http import HTTPStatus
from django.urls import reverse
from django.core.cache import cache

from ..models import Group, Post, Comment

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_author = User.objects.create_user(username='NoNameUser')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user_author,
            text='Тестовый пост 15 символов',
        )
        cls.comment = Comment.objects.create(
            author=cls.user_author,
            text='Тестовый комментарий',
        )

    def setUp(self):
        cache.clear()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_author)

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post_str = Post.objects.get(pk=1)
        response = str(post_str)
        self.assertEqual(response, post_str.text[:15])
        group_str = Group.objects.get(pk=1)
        self.assertEqual(str(group_str), group_str.title)

    def test_comment_posts_only_authorized_client(self):
        """Проверяем, что комментировать посты может
        только авторизованный пользователь
        """
        response = self.authorized_client.get(
            f'/posts/{self.post.id}/comment/',
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_comment(self):
        """Проверяем, что после успешной отправки
        комментарий появляется на странице поста
        """
        comments_count = Comment.objects.count()
        form_data = {
            'author': self.user_author,
            'text': 'Текст комментария',
        }
        response = self.authorized_client.get(
            reverse('posts:add_comment', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Comment.objects.count(), comments_count)
