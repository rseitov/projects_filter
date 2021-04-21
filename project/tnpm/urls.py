from django.urls import path

from tnpm import views

urlpatterns = [

    path('preview/<id>', views.create_sub, name='create_sub')


]