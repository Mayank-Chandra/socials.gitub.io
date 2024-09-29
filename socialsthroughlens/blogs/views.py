from django.shortcuts import render,get_object_or_404
from .models import Post,  Image
from django.http import Http404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import EmailPostForm,CommentForm,SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import(
    SearchVector,
    SearchRank,
    SearchQuery
)
from django.contrib.postgres.search import TrigramSimilarity


def post_list(request,tag_slug=None):
    post_list=Post.published.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])
    paginator=Paginator(post_list,10)
    page_number=request.GET.get('page',1)
    try:
        posts=paginator.page(page_number)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    return render(
        request,
        'blogs/post/list.html',
        {'posts':posts,
         'tag':tag}
    )
    
def post_detail(request,year,month,day,post):
    post=get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    comments=post.comments.filter(active=True)
    form=CommentForm()
    
    #List of Similar Post using Tags
    post_tags_id=post.tags.values_list('id',flat=True)
    similar_posts=Post.published.filter(
        tags__in=post_tags_id
    ).exclude(id=post.id)
    
    similar_posts=similar_posts.annotate(
            same_tags=Count('tags')
    ).order_by('-same_tags','-publish')[:4]
    return render(
        request,
        'blogs/post/detail.html',
        {"post":post,
         'comments':comments,
         'form':form,
         'similar_posts':similar_posts}
    )
    
def post_share(request,post_id):
    post=get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    sent=False
    
    if request.method=='POST':
        form=EmailPostForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject=(
                f'{cd['name']} ({cd['email']})'
                f'recommends you to read{post.title}'
            )
            message=(
                f'Read {post.title} at {post_url}\n\n'
                f'{cd['name']}\'s comments: {cd['comments']}'
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent=True
    else:
        form=EmailPostForm()
    return render(
        request,
        'blogs/post/share.html',
        {
            'post':post,
            'form':form,
            'sent':sent
        }
    )
@require_POST
def post_comment(request,post_id):
    post=get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment=None
    form=CommentForm(data=request.POST)
    if form.is_valid():
        comment=form.save(commit=False)
        comment.post=post
        comment.save()
    return render(
        request,
        'blogs/post/comment.html',
        {
            'post':post,
            'form':form,
            'comment':comment
        }
    )
    
def post_search(request):
    form=SearchForm()
    query=None
    result=[]
    
    if 'query' in request.GET:
        form=SearchForm(request.GET)
        if form.is_valid():
            query=form.cleaned_data['query']
            search_vector=SearchVector('title','body') + SearchVector('body',weight='B')
            search_query=SearchQuery(query)
            result=(
                Post.published.annotate(
                    search=search_vector,
                    rank=SearchRank(search_vector,search_query)
                ).filter(rank__gte=0.1)
            ).order_by('-rank')
    return render(
        request,
        'blogs/post/search.html',
        {
            'form':form,
            'query':query,
            'result':result
        }
    )
def home(request):
    return render(request,
                  'blogs/home.html')
    
def image_list(request,tag_slug=None):
    image_list=Image.published.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        image_list=image_list.filter(tags__in=[tag])
    paginator=Paginator(image_list,8)
    page_number=request.GET.get('page',1)
    try:
        images=paginator.page(page_number)
    except PageNotAnInteger:
        images=paginator.page(1)
    except EmptyPage:
        images=paginator.page(paginator.num_pages)
    return render(
        request,
        'blogs/images/list.html',
        {'images':images,
         'tag':tag}
    )
    
def image_detail(request,image):
    image=get_object_or_404(
        Image,
        status=Image.Status.PUBLISHED,
        slug=image,
        # publish__year=year,
        # publish__month=month,
        # publish__dy=day,
    )
    image_tags_id=image.tags.values_list('id',flat=True)
    similar_images=Image.published.filter(
        tags__in=image_tags_id
    ).exclude(id=image.id)
    
    similar_images=similar_images.annotate(
        same_tags=Count('tags')
    ).order_by('-same_tags','-publish')[:4]
    return render(
        request,
        'blogs/images/detail.html',
        {'image':image,
         'similar_images':similar_images,}
    )