from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from taggit.managers import TaggableManager
from PIL import Image as PILImage
from location_field.models.plain import PlainLocationField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return(
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )
        
        
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT='DF',"Draft"
        PUBLISHED='PB','Published'
        
        
    title=models.CharField(max_length=250)
    slug=models.SlugField(max_length=250,
                          unique_for_date='publish')
    author=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blogs_posts'
    )
    
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )
    objects=models.Manager()
    published=PublishedManager()
    tags=TaggableManager()
    class Meta:
        ordering=['-publish']
        indexes=[
            models.Index(fields=['-publish']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blogs:post_detail", args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug
        ])
    
class Comment(models.Model):
    post=models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name=models.CharField(max_length=80)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    
    class Meta:
        ordering=['created']
        indexes=[
            models.Index(fields=['created']),
        ]
        
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    
class Image(models.Model):
    class Status(models.TextChoices):
        DRAFT='DF','Draft'
        PUBLISHED='PB','Published'
        
        
    title=models.CharField(max_length=200)
    slug=models.SlugField(max_length=200,blank=True)
    author=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='images_post'
    )
    image=models.ImageField(upload_to='images/%Y/%m/%d')
    description=models.TextField(blank=True)
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    city=models.CharField(max_length=255,default='City')
    state=models.CharField(max_length=255,default='State')
    country=models.CharField(max_length=255,default='Country')
    location=models.CharField(max_length=255,default='location')
    status=models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT,
    )
    objects=models.Manager()
    published=PublishedManager()
    tags=TaggableManager()
    class Meta:
        indexes=[
            models.Index(fields=['-publish'])
        ]
        ordering=['-publish']
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img=PILImage.open(self.image.path)
        if img.width > img.height:
            self.orientation='horizontal'
        else:
            self.orientation='vertical'
        super().save(*args,**kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blogs:image_detail", args=[
            # self.publish.year,
            # self.publish.month,
            # self.publish.day,
            self.slug
        ])
    