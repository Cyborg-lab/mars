from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('<int:pk>/enroll/', views.enroll_course, name='enroll_course'),
    path('<int:course_pk>/module/<int:module_pk>/lesson/<int:lesson_pk>/', views.lesson_view, name='lesson_view'),
]
