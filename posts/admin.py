from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_link', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'author')
    search_fields = ('title', 'text', 'author__login', 'author__first_name', 'author__last_name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'text', 'image', 'author')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def author_link(self, obj):
        """Отображает ссылку на автора поста"""
        if obj.author:
            url = reverse('admin:users_user_change', args=[obj.author.id])
            return format_html('<a href="{}">{}</a>', url, obj.author.login)
        return '-'

    author_link.short_description = 'Автор'
    author_link.admin_order_field = 'author__login'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text_preview', 'author_link', 'post_link', 'created_at')
    list_filter = ('created_at', 'post', 'author')
    search_fields = ('text', 'author__login', 'post__title')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Комментарий', {
            'fields': ('text', 'post', 'author')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def text_preview(self, obj):
        """Отображает превью текста комментария"""
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    text_preview.short_description = 'Текст'

    def author_link(self, obj):
        """Отображает ссылку на автора комментария"""
        if obj.author:
            url = reverse('admin:users_user_change', args=[obj.author.id])
            return format_html('<a href="{}">{}</a>', url, obj.author.login)
        return '-'

    author_link.short_description = 'Автор'
    author_link.admin_order_field = 'author__login'

    def post_link(self, obj):
        """Отображает ссылку на пост"""
        if obj.post:
            url = reverse('admin:posts_post_change', args=[obj.post.id])
            return format_html('<a href="{}">{}</a>', url, obj.post.title)
        return '-'

    post_link.short_description = 'Пост'
    post_link.admin_order_field = 'post__title'
