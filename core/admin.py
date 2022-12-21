
from django.contrib import admin
from .models import Post, Comment, Category
from linguist.admin import TranslatableModelAdmin

from import_export.admin import ImportExportModelAdmin


@admin.register(Category)
class CategoryAdmin(TranslatableModelAdmin):
    list_display = ["title", "slug"]
    readonly_fields = ["slug"]


# admin.site.register(Post)
admin.site.register(Post)


# admin.site.register(Comment
admin.site.register(Comment)