from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Comment, Post, Category

class NewComment(forms.ModelForm):

    name_en = forms.CharField(label=_('Name'))
    name_ar = forms.CharField(label=_('Name'))
    email = forms.EmailField(label=_('Email'))
    body_en = forms.CharField(label=_('Your Comment'), widget=forms.Textarea)
    body_ar = forms.CharField(label=_('Your Comment'), widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ('name_en','name_ar', 'email', 'body_en', 'body_ar')


class PostCreateForm(forms.ModelForm):
    title = forms.CharField(label=_('Post title'))
    content = forms.CharField(label=_('Post content'), widget=forms.Textarea)
    media = forms.FileField(label=_('Media File'), widget=forms.ClearableFileInput(attrs={'multiple':True}))
    category = forms.ChoiceField(label=_('Category'))

    class Meta:
        model = Post
        fields = ['title', 'category', 'content', 'media', ]

        widgets = {
        	'category': forms.Select(attrs={'class': 'text-center'}),
        }


class CategoryCreateForm(forms.ModelForm):
    name = forms.CharField(label=_('Category title'))

    class Meta:
        model = Category
        fields = ['name', ]
