from django.urls import path
from authors import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardRecipeList.as_view(), name='dashboard'),
    path(
        'dashboard/create/',
        views.DashboardRecipe.as_view(), name='dashboard_recipe_create'
        ),
    path(
        'dashboard/<int:recipe_id>/edit/',
        views.DashboardRecipe.as_view(), name='dashboard_recipe_edit'
        ),
    path(
        'dashboard/<int:recipe_id>/delete/',
        views.DashboardRecipeDelete.as_view(), name='dashboard_recipe_delete'
        ),
    path(
        'profile/<int:id>/',
        views.ProfileView.as_view(), name='profile'
        ),
]
