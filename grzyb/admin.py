from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from grzyb.models import BlogPost,Comment, Like, Dislike




admin.site.register(Like)
admin.site.register(Dislike)
class BlogPostAdmin(admin.ModelAdmin):          # co ma być wyświetlone w panelu admina
    list_display = ( 'title', 'date_published', 'date_updated', 'author')
    search_fields = ('title', 'author')
    readonly_fields = ('date_published', 'date_updated', 'author','slug','title')
admin.site.register(BlogPost, BlogPostAdmin)

class CommentAdmin(admin.ModelAdmin):          # co ma być wyświetlone w panelu admina
    list_display = ( 'post', 'author', 'body', 'created_on','active','likes','dislikes')
    search_fields = ('author', 'post')
    readonly_fields = ('created_on', 'post', 'author','likes','dislikes')
admin.site.register(Comment,CommentAdmin)


# Register your models here.
