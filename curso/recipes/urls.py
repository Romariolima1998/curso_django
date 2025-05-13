from django.urls import path
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='home'),
    path('recipe/<int:pk>/', views.RecipeDetail.as_view(), name='recipe'),
    path('recipe/category/<int:id>/', views.RecipeCategoryView.as_view(), name='category'),
    path('recipe/search/', views.SearchListView.as_view(), name='search'),

]