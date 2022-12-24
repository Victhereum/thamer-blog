# Generated by Django 3.2 on 2022-12-24 04:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import linguist.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True, unique=True, verbose_name='slug')),
                ('title_en', models.CharField(max_length=32, null=True, verbose_name='name')),
                ('title_ar', models.CharField(max_length=32, null=True, verbose_name='name')),
                ('lang', models.CharField(choices=[('en', 'English'), ('ar', 'Arabic')], default='en', max_length=5, verbose_name='Default Language')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(linguist.mixins.ModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PostTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, help_text='The registered model identifier.', max_length=100, verbose_name='identifier')),
                ('object_id', models.IntegerField(db_index=True, help_text='The object ID of this translation', verbose_name='The object ID')),
                ('language', models.CharField(choices=[('en', 'English'), ('ar', 'Arabic')], db_index=True, default='en', help_text='The language for this translation', max_length=10, verbose_name='language')),
                ('field_name', models.CharField(db_index=True, help_text='The model field name for this translation.', max_length=100, verbose_name='field name')),
                ('field_value', models.TextField(help_text='The translated content for the field.', null=True, verbose_name='field value')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.FileField(blank=True, null=True, upload_to='video/%y', verbose_name='media')),
                ('title_en', models.CharField(max_length=100, null=True, verbose_name='title')),
                ('title_ar', models.CharField(max_length=100, null=True, verbose_name='title')),
                ('content_en', models.TextField(null=True, verbose_name='content')),
                ('content_ar', models.TextField(null=True, verbose_name='content')),
                ('lang', models.CharField(choices=[('en', 'English'), ('ar', 'Arabic')], default='en', max_length=5, verbose_name='Default Language')),
                ('post_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='post date')),
                ('post_update', models.DateTimeField(auto_now=True, verbose_name='post update')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'posts',
                'ordering': ('post_date',),
            },
            bases=(linguist.mixins.ModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Your name', max_length=50, verbose_name='name')),
                ('email', models.EmailField(help_text='Your email', max_length=254, verbose_name='email')),
                ('body', models.TextField(help_text='Your comment', verbose_name='body')),
                ('active', models.BooleanField(default=False)),
                ('comment_date', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.post')),
            ],
            options={
                'ordering': ('-comment_date',),
            },
        ),
    ]
