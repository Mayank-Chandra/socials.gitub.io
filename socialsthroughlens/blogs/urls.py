from django.urls import path
from . import views
from .feeds import LatestPostsFeed
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

app_name='blogs'

urlpatterns = [
    path('blogpost/',views.post_list,name='post_list'),
    path(
        'tag/<slug:tag_slug>/',views.post_list,name='post_list_by_tag'
    ),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
    path('<int:post_id>/share/',views.post_share,name='post_share'),
    path(
        '<int:post_id>/comment/',views.post_comment,name='post_comment'
    ),
    path('feed/',LatestPostsFeed(),name='post_feed'),
    path('search/',views.post_search,name='post_search'),
    path('',views.home,name='home'),
    path('gallery/',views.image_list,name='image_list'),
    path(
        'image/<slug:tag_slug>/',
         views.image_list,
         name='image_list_by_tag'),
    path(
        'gallery/<slug:image>/',
        views.image_detail,
        name='image_detail')

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
