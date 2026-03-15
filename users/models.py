from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import re


class User(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True, unique=False)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    login = models.EmailField(unique=True)
    password = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        self.validate_password()
        self.validate_login()

    def validate_password(self):
        """Валидатор пароля: минимум 8 символов, должна быть цифра"""
        if len(self.password) < 8:
            raise ValidationError("Пароль должен содержать минимум 8 символов.")
        if not re.search(r"\d", self.password):
            raise ValidationError("Пароль должен включать хотя бы одну цифру.")

    def validate_login(self):
        """Валидатор для логина"""
        allowed_domains = ["mail.ru", "yandex.ru"]
        domain = self.login.split("@")[-1].lower()
        if domain not in allowed_domains:
            raise ValidationError(f'Разрешены только домены: {", ".join(allowed_domains)}')

    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.login
