from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Comment
import requests
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from taggit.models import Tag
from django.db.models import Count

# Create your views here.
def home(request):
    return render(request,'home.html',{})


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 5) # 3 posts a page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page isnt an int we show 1st page.
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range show last Page
        posts = paginator.page(paginator.nm_pages)
    return render(request, 'blog/post/list.html',{'page': page, 'posts': posts, 'tag': tag})

class PostListView(ListView):
        queryset = Post.published.all()
        context_object_name = 'posts'
        paginate_by = 3
        template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                    status='published',
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)
    # List of active Comments for post
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # Comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # create new comment object
            new_comment = comment_form.save(commit=False)
            #Assign the current post to comment
            new_comment.post = post
            # Now save comment to database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # list similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request,
                 'blog/post/detail.html',
                  {'post':post,
                  'comments': comments,
                  'new_comment': new_comment,
                  'comment_form': comment_form,
                  'similar_posts': similar_posts})


def post_share(request, post_id):
    # Retrieve post by # ID:
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed password_validation
            cd = form.cleaned_data
            post_url = request.build_absolute_url(post.get_absolute_url())
            subject = '{} ({}) recomends you reading"{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['coments'])
            send_mail(subject, message, 'admin@blog', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
        return render(request, 'blog/post/share.html', {'post': post,
                                                        'form': form,
                                                        'sent': sent})
