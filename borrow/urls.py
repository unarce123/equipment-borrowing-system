from django.urls import path
from . import views

urlpatterns = [
    path('', views.borrow_list, name='borrow_list'),
    path('create/', views.create_borrow, name='create_borrow'),
    path('approve/<int:pk>/', views.approve_borrow, name='approve_borrow'),
    path('reject/<int:pk>/', views.reject_borrow, name='reject_borrow'),
    path('return/<int:pk>/', views.return_borrow, name='return_borrow'),
    path('delete/<int:pk>/', views.delete_borrow, name='delete_borrow'),

    # NOTIFICATIONS
    path('notifications/', views.notifications, name='notifications'),
]