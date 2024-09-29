from django import forms
from .models import Comment
from django.contrib.auth.decorators import login_required

class EmailPostForm(forms.Form):
    name=forms.CharField(max_length=25,widget=forms.TimeInput(attrs={
        'class':'comment_name',
        'placeholder':'Name',
    }))
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'comment_email',
        'placeholder':'Email'
    }))
    to=forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'comment_email',
        'placeholder':'Email'
    }))
    comments=forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class':'comment_body',
            'placeholder':'comment',
            'style':'max-width:150px;max-height:50px'
        })
    )
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['name','email','body']
        widgets={
            'name':forms.TextInput(attrs={
                'placeholder':'Name',
                'class':'comment_name',
            }),
            'email':forms.EmailInput(attrs={
                'placeholder':'Email',
                'class':'comment_email'
            }),
            'body':forms.TextInput(attrs={
                'placeholder':'Body',
                'class':'comment_body',
                'style':'max-height:500px',
            }),
        }

class SearchForm(forms.Form):
    query=forms.CharField(widget=forms.TextInput(attrs={
        'class':'search',
        'placeholder':'Search Query'
    }))
    

