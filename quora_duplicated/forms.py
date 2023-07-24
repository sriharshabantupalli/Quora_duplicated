from django import forms
from .models import Question, Answer, Comment

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

# forms.py
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']
