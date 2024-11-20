from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginpage, name='login'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    # path('delete/<str:habit_name>/', views.delete_habit, name='delete'),
    path('delete/<str:habit_name>/', views.delete_habit, name='delete'),
    path('update/<str:habit_name>/', views.update_habit, name='update'),
    path('edit/<str:habit_name>/', views.edit_habit, name='edit'), 
    path('logout/',views.Logoutview,name="logout"),
    # path('notifications/', views.notifications, name='notifications'),
]
