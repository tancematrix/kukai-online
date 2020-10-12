from django.urls import include, path

from . import views

app_name = "kukai"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
    path('<int:unza_id>/toku/', views.toku, name='toku'),
    path('<int:unza_id>/toku_close/', views.close_toku, name='toku_close'),
    path('<int:unza_id>/save_haiku/', views.save_haiku, name='save_haiku'),
    path('<int:unza_id>/senku/', views.senku, name='senku'),
    path('<int:unza_id>/save_senku/', views.save_senku, name='save_senku'),
    path('<int:unza_id>/senku_close/', views.close_senku, name='senku_close'),
    path('<int:unza_id>/<int:ku_id>/edit', views.edit_haiku, name='edit_haiku'),
    path('<int:unza_id>/<int:ku_id>/delete', views.delete_haiku, name='delete_haiku'),
]