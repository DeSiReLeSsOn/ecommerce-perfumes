from django import forms
from .models import Review, Comment

class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите ваш отзыв',
            'rows': 3,
        })



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите ваш комментарий',
            'rows': 3,
        })