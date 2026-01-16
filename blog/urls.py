from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_blog, name='add_blog'),
    path('blog/<int:id>/', views.blog_detail, name='blog_detail'),
    path('edit/<int:id>/', views.edit_journey, name='edit_journey'),
    path('delete/<int:id>/', views.delete_journey, name='delete_journey'),
    path('like/<int:id>/', views.like_journey, name='like'),

    # ✅ Registration
    path('accounts/register/', views.register, name='register'),
]
