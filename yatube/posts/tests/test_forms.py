from django.test import Client, TestCase, override_settings
from django.urls import reverse
from http import HTTPStatus
from posts.forms import PostForm
from posts.models import Post, Group, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import tempfile
from django.core.cache import cache


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
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

        @classmethod
        def tearDownClass(cls):
            super().tearDownClass(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        cache.clear()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_author)

    def test_create_post(self):
        """Проверка валидная форма создаёт запись в Post"""
        posts_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Тестовый пост',
            'group': self.group.id,
            'image': uploaded,
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
        post = Post.objects.latest('id')
        self.assertTrue(Post.objects.filter(
            text='Тестовый пост',
            group=self.group.id,
            image=post.image,
        ).exists())

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
