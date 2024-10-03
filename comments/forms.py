from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6, 'cols': 60, 'placeholder': 'نظرات خود را اینجا تایپ کنید...'}),
        }
        labels = {
            'content': '',
        }
