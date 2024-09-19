from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


# class User(AbstractUser):
#     name = models.CharField(max_length=200, null=True)
#     email = models.EmailField(unique=True, null=True)
#     bio = models.TextField(null=True)

#     avatar = models.ImageField(null=True, default='avatar.svg')

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []


class Catalog(models.Model):

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Содержимое")
    photo = models.ImageField(
        upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(
        auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    year = models.ForeignKey('Category', on_delete=models.PROTECT,  null=True)

    class Meta:
        ordering = ['-time_update', '-time_create']

    def __str__(self):
        return self.title


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):

    host = models.ForeignKey(User,
                             on_delete=models.CASCADE, null=True)
    topic = models.ForeignKey(
        Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, verbose_name='Name')

    description = models.TextField(
        null=True, blank=True, verbose_name='Description')
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now=True)
    room = models.ForeignKey(
        "Catalog",  on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'year_slug': self.slug})

    class Meta:
        verbose_name = 'Школьная бибилиотека'
        verbose_name_plural = 'Электронный каталог'


class Message(models.Model):
    # User models https://docs.djangoproject.com/en/4.0/ref/contrib/auth/
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, verbose_name="", on_delete=models.CASCADE)
    catalog = models.ForeignKey(
        Catalog, verbose_name="", on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True, verbose_name='')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]
