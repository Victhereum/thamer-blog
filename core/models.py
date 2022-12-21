from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _
from linguist.metaclasses import ModelMeta as LinguistMeta
from linguist.mixins import ManagerMixin as LinguistManagerMixin
from linguist.models.base import Translation

def slugify(str):
    str = str.replace(" ", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("؟", "")
    return str

class LanguagesChoices(models.TextChoices):
    English = ("en", _("English"))
    Arabic = ("ar", _("Arabic"))

class PostTranslation(Translation):
    class Meta:
        abstract = False

class PostGenericManager(LinguistManagerMixin, models.Manager):
    pass


class Category(models.Model, metaclass=LinguistMeta):

    slug = models.SlugField(_('slug'),unique=True, allow_unicode=True, blank=True, null=True)
    title = models.CharField(_('name'),max_length=32, null=True)
    lang = models.CharField(max_length=5, verbose_name="Default Language", default=LanguagesChoices.English, choices=LanguagesChoices.choices)
    objects = PostGenericManager()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        linguist = {
            'identifier': 'category',
            'fields': ('title',),
            'default_language': 'en',
            'default_language_field': 'lang',
            'decider': PostTranslation,
        }

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        # super().save(*args, **kwargs)
        if not self.pk:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        # return '/detail/{}'.format(self.pk)
        return reverse('category', args=[self.slug])

class Post(models.Model, metaclass=LinguistMeta):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name=_('category'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('author'),)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation', verbose_name=_('hit_count_generic'),)
    media = models.FileField(_('media'),upload_to="video/%y", null=True, blank=True)
    title = models.CharField(_('title'),max_length=100, null=True)
    content = models.TextField(_('content'), null=True)

    lang = models.CharField(max_length=5, verbose_name="Default Language", default=LanguagesChoices.English, choices=LanguagesChoices.choices)
    post_date = models.DateTimeField(_('post date'),default=timezone.now)
    post_update = models.DateTimeField(_('post update'),auto_now=True)

    objects = PostGenericManager()

    class Meta:
        ordering = ('post_date',)
        verbose_name = _('Post')
        verbose_name_plural = _('posts')
        linguist = {
            'identifier': 'post',
            'fields': ('title', "content",),
            'default_language': 'en',
            'default_language_field': 'lang',
            'decider': PostTranslation,
        }

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        # return '/detail/{}'.format(self.pk)
        return reverse('detail', args=[self.pk])

class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')

    name = models.CharField(_('name'),max_length=50, help_text=_('Your name'),)
    email = models.EmailField(_('email'), help_text=_('Your email'),)
    body = models.TextField(_('body'), help_text=_('Your comment'),)
    active = models.BooleanField(default=False)
    comment_date = models.DateTimeField(auto_now_add=True,)
    
    def __str__(self):
        return 'commented {} on {}.'.format(self.name, self.post)

    class Meta:
        ordering = ('-comment_date',)