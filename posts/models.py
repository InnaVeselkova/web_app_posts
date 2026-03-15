from datetime import date

from django.db import models
from django.core.exceptions import ValidationError

from users.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    FORBIDDEN_WORDS = ['ерунда', 'глупость', 'чепуха']

    def clean(self):
        super().clean()
        self.validate_author_age()
        self.validate_title()

    def validate_author_age(self):
        """Проверка: автор должен быть старше 18 лет"""
        if self.author:
            today = date.today()
            age = today.year - self.author.birth_date.year - (
                (today.month, today.day) < (self.author.birth_date.month, self.author.birth_date.day)
            )
            if age < 18:
                raise ValidationError('Автор должен быть старше 18 лет.')

    def validate_title(self):
        """Проверка: заголовок не должен содержать запрещенные слова"""
        title_lower = self.title.lower()
        for word in self.FORBIDDEN_WORDS:
            if word in title_lower:
                raise ValidationError(f'Заголовок содержит запрещенное слово: "{word}"')

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author.login} on {self.post.title}'
