from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_add_trainees, name='trainee.list_add'),
    path('<int:pk>', views.get_update_delete_trainee, name='trainee.get_update_delete'),
    path('search/', views.search_trainees, name='trainee.search'),
]
