from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('login/', views.login_user, name='login'),
    # path('logout/', LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile_update/', views.profile_update, name='profile_update'),
    #Delete an invoice
	path('profile/delete/<str:pk>',views.comment_del, name='comment_del'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)