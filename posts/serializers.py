from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Post, Comment
from users.models import User


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для постов"""

    author = UserSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)
    author_login = serializers.CharField(source="author.login", read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "text", "image", "author", "author_id", "author_login", "created_at", "updated_at")
        read_only_fields = ("id", "author", "created_at", "updated_at")

    def validate_title(self, value):
        """Валидация заголовка - проверка запрещенных слов"""
        forbidden_words = ["ерунда", "глупость", "чепуха"]
        title_lower = value.lower()
        for word in forbidden_words:
            if word in title_lower:
                raise serializers.ValidationError(f'Заголовок содержит запрещенное слово: "{word}"')
        return value

    def validate_author_id(self, value):
        """Валидация автора - проверка возраста"""
        try:
            author = User.objects.get(id=value)
            from datetime import date

            today = date.today()
            age = (
                today.year
                - author.birth_date.year
                - ((today.month, today.day) < (author.birth_date.month, author.birth_date.day))
            )
            if age < 18:
                raise serializers.ValidationError("Автор должен быть старше 18 лет.")
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден.")


class PostCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания поста (автор - текущий пользователь)"""

    class Meta:
        model = Post
        fields = ("title", "text", "image")

    def validate_title(self, value):
        """Валидация заголовка"""
        forbidden_words = ["ерунда", "глупость", "чепуха"]
        title_lower = value.lower()
        for word in forbidden_words:
            if word in title_lower:
                raise serializers.ValidationError(f'Заголовок содержит запрещенное слово: "{word}"')
        return value

    def create(self, validated_data):
        """Создаем пост с текущим пользователем как автором"""
        from datetime import date

        request = self.context.get("request")
        author = request.user

        # Проверяем возраст автора
        today = date.today()
        age = (
            today.year
            - author.birth_date.year
            - ((today.month, today.day) < (author.birth_date.month, author.birth_date.day))
        )
        if age < 18:
            raise serializers.ValidationError("Автор должен быть старше 18 лет.")

        validated_data["author"] = author
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев"""

    author = UserSerializer(read_only=True)
    post_title = serializers.CharField(source="post.title", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "post", "post_title", "created_at", "updated_at")
        read_only_fields = ("id", "author", "created_at", "updated_at")


class CommentCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания комментария"""

    class Meta:
        model = Comment
        fields = ("text", "post")

    def create(self, validated_data):
        """Создаем комментарий с текущим пользователем как автором"""
        request = self.context.get("request")
        validated_data["author"] = request.user
        return super().create(validated_data)
