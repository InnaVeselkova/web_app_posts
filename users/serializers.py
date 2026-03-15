from rest_framework import serializers
import re
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Универсальный сериализатор для пользователя"""

    class Meta:
        model = User
        fields = [
            'id',
            'login',
            'password',
            'phone_number',
            'birth_date',
            'created_at',
            'updated_at'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

    def validate_password(self, value):
        """Валидация пароля: минимум 8 символов, должна быть цифра"""
        if len(value) < 8:
            raise serializers.ValidationError('Пароль должен содержать минимум 8 символов.')
        if not re.search(r'\d', value):
            raise serializers.ValidationError('Пароль должен включать хотя бы одну цифру.')
        return value

    def validate_login(self, value):
        """Валидация логина: разрешены только mail.ru и yandex.ru"""
        allowed_domains = ['mail.ru', 'yandex.ru']
        domain = value.split('@')[-1].lower()
        if domain not in allowed_domains:
            raise serializers.ValidationError(
                f'Разрешены только домены: {", ".join(allowed_domains)}'
            )
        return value

    def create(self, validated_data):
        """Создание пользователя с хешированием пароля"""
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """Обновление пользователя"""
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
