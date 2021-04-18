from django.urls import path
from writer import views

urlpatterns = [
    path('passion/become-a-writer/', views.signup_writer, name='signup_writer'),
    path('writer/<str:name>/', views.writer_profile, name='writer_profile'),
]