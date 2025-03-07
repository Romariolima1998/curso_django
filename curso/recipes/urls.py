from django.urls import path
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/<int:id>/', views.recipe, name='recipe'),
    path('recipe/category/<int:id>/', views.category, name='category'),
    path('recipe/search/', views.search, name='search'),

]