from .models import User, Update, Resource, Submission, Assignment
from .models import Subject, Post, Comment, Lesson, Notification

from django import forms
from django.forms import ModelForm

class UpdateForm(ModelForm):
    class Meta:
        model = Update
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows':4, 'cols':60}),
        }

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows':4, 'cols':60}),
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows':4, 'cols':60}),
        }

class ResourceForm(ModelForm):
    class Meta:
        model = Resource
        fields = ['subject', 'doc']

class AssignmentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # ensure that the teacher can only create for his/her subjects
        queryset = Subject.objects.all()
        if kwargs.get('subjects'):
            queryset = kwargs.pop('subjects')
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset = queryset

    class Meta:
        model = Assignment
        fields = ['deadline', 'subject', 'title', 'description']
        widgets = {
            'deadline': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'class':'datetimefield'}),
            'description': forms.Textarea(attrs={'rows':2, 'cols':60}),
        }

class LessonForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # ensure that the teacher can only create for his/her subjects
        queryset = Subject.objects.all()
        if kwargs.get('subjects'):
            queryset = kwargs.pop('subjects')
        super(LessonForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset = queryset

    class Meta:
        model = Lesson
        fields = ['subject', 'title', 'url']

class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = ['doc']