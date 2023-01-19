# from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from http import HTTPStatus
from posts.forms import PostForm
from posts.models import Post, Group, User


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_author = User.objects.create_user(username='NoNameUser')
        cls.group = Group.objects.create(
            title='Тестовое группа',
            slug='test-slug',
            description='Тестовое описание',
        )

        cls.post = Post.objects.create(
            author=cls.user_author,
            text='Тестовый пост',
            group=cls.group,
        )

        cls.form = PostForm

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_author)

    def test_create_post(self):
        """Проверка создаётся ли новая запись в базе данных"""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый пост',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response,
                             reverse('posts:profile',
                                     kwargs={'username': 'NoNameUser'}))
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_edit_post(self):
        """Происходит изменение поста с post_id в базе данных"""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Изменённый текст поста',
            'author': self.user_author,
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', args=(self.post.id, )),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response,
                             reverse('posts:post_detail',
                                     args=(self.post.id, )))
        edit_post = Post.objects.all().last()
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertEqual(edit_post.text, 'Изменённый текст поста',)
        self.assertEqual(edit_post.author, self.user_author)
