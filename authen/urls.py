from django.urls import path
from .views import (
    registerUser,
    MyTokenObtainPairView,
    updateUserProfile,
    getUserProfile,
    getUsers,
    getUserById,
    deleteUser,
    updateUser
)

urlpatterns = [
    path('register/', registerUser, name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', getUserProfile, name='user_profile'),
    path('profile/update/', updateUserProfile, name='update_user_profile'),
    path('users/', getUsers, name='get_users'),
    path('users/<int:pk>/', getUserById, name='get_user_by_id'),
    path('users/<int:pk>/delete/', deleteUser, name='delete_user'),
    path('users/<int:pk>/update/', updateUser, name='update_user'),
]
