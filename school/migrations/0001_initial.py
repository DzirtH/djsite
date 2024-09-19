# Generated by Django 4.0.4 on 2022-06-19 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('content', models.TextField(blank=True, verbose_name='Содержимое')),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('is_published', models.BooleanField(default=True, verbose_name='Публикация')),
            ],
            options={
                'ordering': ['-time_update', '-time_create'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Школьная бибилиотека',
                'verbose_name_plural': 'Электронный каталог',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('host', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('participants', models.ManyToManyField(blank=True, related_name='participants', to=settings.AUTH_USER_MODEL)),
                ('topic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.topic')),
            ],
            options={
                'ordering': ['-updated', '-created'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.catalog', verbose_name='')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.room', verbose_name='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated', '-created'],
            },
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.catalog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='catalog',
            name='year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='school.category'),
        ),
    ]
