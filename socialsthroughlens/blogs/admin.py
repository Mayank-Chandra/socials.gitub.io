from django.contrib import admin
from django.utils.html import format_html
from .models import Post,Comment,Image


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    show_facets = admin.ShowFacets.ALWAYS
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=['name','email','post','created','active']
    list_filter=['active','created','updated']
    search_fields=['name','email','body']
    
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    def image_tag(self,obj):
        return format_html('<img src="{}" style="max-width:200px;max-height:200px"/>'.format(obj.image.url))
    list_display=['title','slug','author','publish','status','image_tag']
    list_filter=['status','created','publish','author']
    search_fields=['title','body']
    prepopulated_fields={'slug':('title',)}
    raw_id_fields=['author']
    date_hierarchy='publish'
    ordering=['status','publish']