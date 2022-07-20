from django.urls import path
from grzyb.views import create_blog_view, detail_blog_view, like_dislike_view, deletecom_view, deletblog_view, editblog_view, like_dislike_blog_view

app_name = 'grzyb'

urlpatterns = [
    path('create/', create_blog_view, name="create"),
    path('<slug>/',detail_blog_view, name="detail"),
    path('<slug>/add/<lid>/<comment>',like_dislike_view, name="likes"),
    path('<slug>/blog/<lid>',like_dislike_blog_view, name="blog-likes"),
    path('<slug>/deletecom/<comment>',deletecom_view, name="deletecom"),
    path('<slug>/deleteblog',deletblog_view, name="deleteblog"),
    path('<slug>/editblog',editblog_view, name="editblog"),
]