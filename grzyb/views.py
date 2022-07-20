from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from grzyb.models import BlogPost,Comment, Like, Dislike, LikeBlog,DislikeBlog
from grzyb.forms import CreateBlogPostForm, CommentForm
from account.models import Moje_Konto
from django.db.models import Count
# Create your views here.


def create_blog_view(request):

    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    form = CreateBlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit = False)
        author = Moje_Konto.objects.filter(email = user.email).first()
        obj.author = author
        obj.save()
        form = CreateBlogPostForm()
    context['form'] = form

    return render (request, "grzyb/create_grzyb_blog.html",context)

def like_dislike_view(request, slug,comment,lid):
    user = request.user

    if user.is_authenticated:
        if Comment.objects.filter(id = comment).exists():
            Komment= get_object_or_404(Comment, id=comment)
            if lid=="like":
                if Like.objects.filter(Comment = Komment,Moje_Konto=user).exists():
                    Like.objects.filter(Comment = Komment,Moje_Konto = user).delete()
                else:
                    if Dislike.objects.filter(Comment = Komment,Moje_Konto=user).exists():
                        Dislike.objects.filter(Comment = Komment,Moje_Konto = user).delete()

                    a = Like(Comment = Komment,Moje_Konto = user)
                    a.save()
            elif lid=="dislike":
                if Dislike.objects.filter(Comment = Komment,Moje_Konto=user).exists():
                    Dislike.objects.filter(Comment = Komment,Moje_Konto = user).delete()
                else:
                    if Like.objects.filter(Comment = Komment,Moje_Konto=user).exists():
                        Like.objects.filter(Comment = Komment,Moje_Konto = user).delete()
                    a = Dislike(Comment = Komment,Moje_Konto = user)
                    a.save()


def like_dislike_blog_view(request, slug,lid):
    user = request.user

    if user.is_authenticated:
        if BlogPost.objects.filter(slug=slug).exists():
            Post= get_object_or_404(BlogPost, slug=slug)
            if lid=="like":
                if LikeBlog.objects.filter(BlogPost = Post,Moje_Konto=user).exists():
                    LikeBlog.objects.filter(BlogPost = Post,Moje_Konto = user).delete()
                else:
                    if DislikeBlog.objects.filter(BlogPost = Post,Moje_Konto=user).exists():
                        DislikeBlog.objects.filter(BlogPost = Post,Moje_Konto = user).delete()

                    a = LikeBlog(BlogPost = Post,Moje_Konto = user)
                    a.save()
            elif lid=="dislike":
                if DislikeBlog.objects.filter(BlogPost = Post,Moje_Konto=user).exists():
                    DislikeBlog.objects.filter(BlogPost = Post,Moje_Konto = user).delete()
                else:
                    if LikeBlog.objects.filter(BlogPost = Post,Moje_Konto=user).exists():
                        LikeBlog.objects.filter(BlogPost = Post,Moje_Konto = user).delete()
                    a = DislikeBlog(BlogPost = Post,Moje_Konto = user)
                    a.save()



    return redirect('grzyb:detail',slug=slug)

def deletecom_view(request,slug,comment):
    user = request.user

    if user.is_authenticated:
        if Comment.objects.filter(id = comment,author = user).exists():
            Comment.objects.filter(id = comment,author = user).delete()
    return redirect('grzyb:detail',slug=slug)

def deletblog_view(request,slug):
    user = request.user
    if user.is_authenticated:
        if BlogPost.objects.filter(slug=slug,author=user).exists():
            BlogPost.objects.filter(slug=slug,author=user).delete()
    return redirect('home')


def editblog_view(request,slug):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
    blog_post = get_object_or_404(BlogPost, slug=slug)
    form = CreateBlogPostForm(request.POST or None, request.FILES or None,instance = blog_post)
    if form.is_valid():
        form.initial = {
                    "title": request.POST['title'],
        }
        obj = form.save(commit = False)
        author = Moje_Konto.objects.filter(email = user.email).first()
        obj.author = author
        obj.save()
        form = CreateBlogPostForm()
    context['form'] = form

    return render (request, "grzyb/create_grzyb_blog.html",context)              







def detail_blog_view(request, slug):
    context = {}


    blog_post = get_object_or_404(BlogPost, slug=slug)
    context['blog_post'] = blog_post
    comments = blog_post.comments.filter(active=True)
    new_comment = None
    user = request.user
    blog_post.likes = LikeBlog.objects.filter(BlogPost = blog_post).count()
    blog_post.dislikes = DislikeBlog.objects.filter(BlogPost = blog_post).count()
    blog_post.save()
    for comment in comments:
        comment.likes = Like.objects.filter(Comment = comment).count()
        comment.dislikes = Dislike.objects.filter(Comment = comment).count()
        comment.save()

    if request.method == 'POST':

        comment_form = CommentForm(data=request.POST)  
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.blog_post = blog_post
            author = Moje_Konto.objects.filter(username = user.username).first()

            new_comment.post = blog_post
            new_comment.author = author
            new_comment.save()
            


    else:
        comment_form = CommentForm()
    comments = blog_post.comments.filter(active=True)
    context['user'] = user
    context['comment_form'] = comment_form
    context['comments'] = comments


    return render(request, 'grzyb/detail.html',context)

def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = BlogPost.objects.filter(
                Q(title__icontains=q),
                Q(body__icontains=q)
            ).distinct()
        for post in posts:
            queryset.append(post)
    return list(set(queryset))