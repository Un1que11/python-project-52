from task_manager.users import views

from django.urls import path

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/create/', views.UserCreateView.as_view(), name='create'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='delete'),
    # path('login/', views.LoginUserView.as_view(), name='login'),
    # path('logout/', views.LogoutUsersView.as_view(), name='logout'),
]
