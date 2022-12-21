from django.urls import path
from . import views
from .views import PostCreateView, PostUpdateView, PostDeleteView, CategoryCreateView

urlpatterns = [
    path('', views.home, name='home'),
    path("search", views.search, name="search"),
    path('about/', views.about, name='about'),
    path('detail/<int:post_id>/', views.post_detail, name='detail'),
    path('new_post/', PostCreateView.as_view(), name='new_post'),
    path('detail/<slug:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('detail/<slug:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('new_category/', CategoryCreateView.as_view(), name='new_category'),
    path("categories", views.categories, name="categories"),
    path(r"categories/<slug:slug>/", views.category, name="category"),
]