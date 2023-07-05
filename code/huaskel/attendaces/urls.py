from django.urls import path, include

from . import views

urlpatterns = [
    # Index view
    path('', views.index, name = 'attendances'),
    path('courses/', views.courses, name = 'courses'),
    # path('attendaces/', views.index, name = 'attendaces'),
    path('course/<str:course_code>', views.course, name = 'course')
]
