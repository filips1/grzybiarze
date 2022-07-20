from django import forms

from grzyb.models import BlogPost,Comment

class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image']
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
                  
   
        fields = ('body',)
    def clean(self):
        if self.is_valid():
            body = self.cleaned_data['body']




