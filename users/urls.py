from django.urls import include, path

from users import views

urlpatterns = [
    path('userlist/', views.UserView.as_view(), name='user_list_view'),
    path('usercreate/', views.UserCreateView.as_view(), name='user_create_view'),
    path('userdelete/<int:pk>/', views.UserDeleteView.as_view(),
         name='user_delete_view'),
    path('userupdate/<int:pk>/', views.UserUpdateView.as_view(),
         name='user_update_view'),
]
