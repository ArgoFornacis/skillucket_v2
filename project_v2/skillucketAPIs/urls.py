from django.urls import path
from .views import RegisterApi, LoginApi, CategoryListCreateApi, CategoryByIdApi
app_name = 'api'

urlpatterns = [
    path('register/', RegisterApi.as_view(), name='register'),
    path('login/', LoginApi.as_view(), name='login'),
    path('category/', CategoryListCreateApi.as_view(), name='category'),
    path('category/<int:category_id>', CategoryByIdApi.as_view(), name='category_details'),
    # todo: skill urls
]
