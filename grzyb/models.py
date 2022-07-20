from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from random import randint
from account.models import Moje_Konto

# Create your models here.

def upload_location(instance, filename, **kwargs):
    file_path = 'grzyb_blog_image/{author_id}/{title}-{filename}'.format(
                author_id = str (instance.author_id), title=str(instance.title), filename = filename
        )
    return file_path

class BlogPost(models.Model):

    title = models.CharField(max_length=60, null=False, blank=False, verbose_name='Tytuł')
    body = models.TextField(max_length=5000, null=False, blank = False, verbose_name='opis')
    image = models.ImageField(upload_to = upload_location,null=False, blank=False, verbose_name='obrazek')
    date_published = models.DateTimeField(auto_now_add=True, verbose_name='data publickacji')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='data aktualizacji')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,verbose_name='autor')
    slug = models.SlugField(blank=True, unique=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name='Post'
        verbose_name_plural = 'Posty'

@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username+"-"+ instance.title + str(randint(0,99999999999)))

pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)

class Comment(models.Model):
    post = models.ForeignKey(BlogPost,on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='autor')
    body = models.TextField("opis")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='stworzone')
    active = models.BooleanField(default=True, verbose_name='aktywne')
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    class Meta:
        verbose_name='Komentarz'
        verbose_name_plural = 'Komentarze'
        ordering = ['created_on']

    def __str__(self):
        return 'komentarz o tytule {} zeobiony przez {}'.format(self.body, self.author.username)

class Like(models.Model):
    Comment = models.ForeignKey(Comment ,on_delete=models.CASCADE,verbose_name='Komentarz')
    Moje_Konto = models.ForeignKey(Moje_Konto, on_delete=models.CASCADE,verbose_name='Moje Konto')

class Dislike(models.Model):
    Comment = models.ForeignKey(Comment ,on_delete=models.CASCADE, verbose_name='Komentarz')
    Moje_Konto = models.ForeignKey(Moje_Konto, on_delete=models.CASCADE, verbose_name='Moje_Konto')

class LikeBlog(models.Model):
    BlogPost = models.ForeignKey(BlogPost ,on_delete=models.CASCADE)
    Moje_Konto = models.ForeignKey(Moje_Konto, on_delete=models.CASCADE,verbose_name='Moje Konto')

class DislikeBlog(models.Model):
    BlogPost = models.ForeignKey(BlogPost ,on_delete=models.CASCADE)
    Moje_Konto = models.ForeignKey(Moje_Konto, on_delete=models.CASCADE, verbose_name='Moje_Konto')
