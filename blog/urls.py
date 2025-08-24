from django.urls import path
from blog import views

urlpatterns = [
    path('', views.get_route, name='get_route'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:id>/', views.blog, name='blog_detail'),
    path('details/', views.details, name='details'),
]