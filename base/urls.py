from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('logoutadmin/', views.logoutadmin, name='logoutadmin'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('adminPanelUser/', views.adminPanelUser, name='adminPanelUser'),
    path('update_user/<str:pk>/', views.updateUser, name='update_user'),
    path('delete_user/<str:pk>/', views.deleteUser, name='delete_user'),

]