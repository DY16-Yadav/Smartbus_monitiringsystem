from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),       
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('api/send/', views.receive_data, name='receive_data'),
    path('api/get/', views.get_data, name='get_data'),

    path('api/history/latest/', views.history_latest, name='history_latest'),
    path('api/history/timely/', views.history_timely, name='history_timely'),
]
