from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
urlpatterns = [
    path('', views.Index.as_view(), name = 'index'),
    path('task/<int:pk>', views.TaskDetail.as_view(), name ='task'),
    path('create/', views.TaskCreate.as_view(), name ='create'),
    path('update/<int:pk>', views.UpdateView.as_view(), name ='update'),
    path('delete/<int:pk>', views.DeleteView.as_view(), name ='delete'),
    path('login/', views.CustomLoginView.as_view(), name ='login'),
    path('logout/', LogoutView.as_view(next_page = 'login'), name ='logout'),
    path('register/', views.RegisterPage.as_view(), name = 'register'),
    path('color/', views.black_white, name='color')

]
