from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from posts.models import Post, Group, User
from django.urls import reverse


User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_author = User.objects.create_user(username='StasBasov')
        cls.group = Group.objects.create(
            title='Заголовок',
            slug='test-slug',
            description='Тестовое описание',
        )
        for i in range(1, 11):
            cls.post = Post.objects.create(
                text=f'Тестовый пост {i}',
                author=cls.user_author,
                group=cls.group,
            )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='NoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author_client = Client()
        self.author_client.force_login(self.user_author)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон"""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': 'test-slug'}): 'posts/group_list.html',
            reverse('posts:profile',
                    kwargs={'username': 'StasBasov'}): 'posts/profile.html',
            reverse('posts:post_detail',
                    kwargs={'post_id': '1'}): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit',
                    kwargs={'post_id': '1'}): 'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.author_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_first_page_contains_ten_records(self):
        """Проверка работы Paginator"""
        pages_names = {
            'posts:index': {},
            'posts:group_list': {'slug': 'test-slug'},
            'posts:profile': {'username': self.user_author.username},
        }
        for page, args in pages_names.items():
            with self.subTest(page=page):
                response = self.author_client.get(reverse(page, kwargs=args))
                self.assertEqual(len(response.context['page_obj']), 10)

    def test_post_appers_on_pages_with_group(self):
        """Если при создании поста указать группу,
        то пост появляется на страницах
        """
        pages_names = (
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': 'test-slug'}),
            reverse('posts:profile', kwargs={'username': self.user_author}),
        )
        self.post = Post.objects.create(
            text='Тестовый пост 1',
            author=self.user_author,
            group=self.group,
        )
        for page in pages_names:
            with self.subTest(page=page):
                response = self.authorized_client.get(page)
                new_post = response.context['page_obj'][0]
                post_text = new_post.text
                post_group = new_post.group
                post_author = new_post.author
                self.assertEqual(post_text,
                                 'Тестовый пост 1')
                self.assertEqual(post_group, self.group)
                self.assertEqual(post_author, self.user_author)
