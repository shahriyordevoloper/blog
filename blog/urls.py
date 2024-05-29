from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="home"),
    path('login/', user_login, name='login'),
    path('signup/', user_signup, name='signup'),
    path('logout/', user_logout, name='logout'),
    path('most_view/', Most_views.as_view(), name='book-list-create'),
    path('most_mount/', Most_mount.as_view(), name='book-list-create'),
    path('add/', Post_add.as_view(), name='book-list-create'),
    path('explanation/', Explanation.as_view(), name='book-list-create'),
    path('parents/<int:pk>/', ParentDetailAPIView.as_view(), name='parent-detail'),
    # Login sigin 
    path('api/signup/', UserSignupView.as_view(), name='signup'),
    path('api/login/', UserLoginView.as_view(), name='login'),

]
