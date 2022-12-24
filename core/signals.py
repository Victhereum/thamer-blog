from django_translate_po.translate import PoTranslator
from django_translate_po.translator_functions import select_translator_function

from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Category, Comment, Post, LanguagesChoices

translator_function = select_translator_function("Google")


@receiver(post_save, sender=Post)
def translate_new_post(sender, instance, created, **kwargs):
    """Translates the post from the default language to another"""
    if created:
        if instance.lang == LanguagesChoices.English:
        # Translate the title and content
            title = translator_function(str(instance.name), source_code="en", target_code="ar")
            content = translator_function(str(instance.body), source_code="en", target_code="ar")

            # add them to the arabic virtual_instance of the
            instance.title_ar = title
            instance.content_ar = content
        else:
        # Translate the title and content
            title = translator_function(str(instance.name), source_code="ar", target_code="en")
            content = translator_function(str(instance.body), source_code="ar", target_code="en")

            # add them to the arabic virtual_instance of the
            instance.title_en = title
            instance.content_en = content
        instance.save()


@receiver(post_save, sender=Category)
def translate_new_category(sender, instance, created, **kwargs):
    """Translates the category from the default language to another"""
    if created:
        if instance.lang == LanguagesChoices.English:
            # Translate the title
            title = translator_function(str(instance.title), source_code="en", target_code="ar")

            # add them to the arabic virtual_instance of the
            instance.title_ar = title
        else:
            # Translate the title
            title = translator_function(str(instance.title), source_code="ar", target_code="en")

            # add them to the arabic virtual_instance of the
            instance.title_en = title

        # Now save the instance
        instance.save()

@receiver(post_save, sender=Comment)
def translate_new_comment(sender, instance, created, **kwargs):
    """Translates the comment from the default language to another"""
    if created:
        if instance.lang == LanguagesChoices.English:
        # Translate the name and body
            name = translator_function(str(instance.name), source_code="en", target_code="ar")
            body = translator_function(str(instance.body), source_code="en", target_code="ar")

            # add them to the arabic virtual_instance of the
            instance.name_ar = name
            instance.body_ar = body
        else:
        # Translate the name and body
            name = translator_function(str(instance.name), source_code="ar", target_code="en")
            body = translator_function(str(instance.body), source_code="ar", target_code="en")

            # add them to the english virtual_instance of the
            instance.name_en = name
            instance.body_en = body

        # Now save the instance
        instance.save()
