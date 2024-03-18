from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('registerteacher/', RegisterTeacherView.as_view(), name="register_teacher"),
    path('registeradmin/', RegisterAdminView.as_view(), name="register_admin"),
    path('registersuper/', RegisterSuperUserView.as_view(), name="registersuper"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('user/', UserListView.as_view(), name="user"),
    path('userupdate/', UserVarifyView.as_view(), name="uservarify"),
    path('token/refresh/', TokenRefreshView.as_view(), name="uservarify"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    

]