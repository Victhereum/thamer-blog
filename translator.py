from django_translate_po.translate import PoTranslator

po_translator = PoTranslator("./locale/ar/LC_MESSAGES/django.po", translator_service="Google", source_code="en", target_code="ar")
po_translator.generate_text_for_untranslated()

