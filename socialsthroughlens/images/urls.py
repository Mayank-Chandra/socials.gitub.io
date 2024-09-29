from django.urls import path
from . import views
from django.urls import reverse_lazy

app_name='images'

urlpatterns = [
    path('create/',views.image_create,name='create'),
    path(
        'detail/<int:id>/<slug:slug>/',
        views.image_detail,
        name='detail'
    ),
    path('like/',views.image_like,name='like'),
    path('',views.image_list,name='list'),
    path('upload/',views.upload_image,name='upload'),
    path('upload-successful/',views.upload_success,name='upload_success')
]
