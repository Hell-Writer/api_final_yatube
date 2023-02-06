from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=200)
    slug = models.SlugField(
        verbose_name='Адрес',
        unique=True)
    description = models.TextField(
        verbose_name='Описание',)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    group = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.CASCADE,
        related_name='group')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments', null=True)
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    def __str__(self):
        return self.following.username[:25]

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'], name='name')
        ]
