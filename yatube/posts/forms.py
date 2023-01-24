from django import forms
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('text', 'group', 'image')
        group = forms.ModelChoiceField(
            queryset=Post.objects.all(), required=False, to_field_name='group')
        widgets = {
            "text": forms.Textarea()
        }
        labels = {
            "text": "Текст поста", "group": "Группа"
        }
        help_text = {
            "text": "Текст нового поста",
            "group": "Группа, к которой будет относиться пост",
        }


class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('text',)
        labels = {
            'text': 'Текст комментария'
        }
