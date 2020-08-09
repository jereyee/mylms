from django.contrib import admin

from .models import User, Update, Resource, Submission, Assignment
from .models import Subject, Post, Comment, Lesson, Notification

# Register your models here.
admin.site.register(User)
admin.site.register(Update)
admin.site.register(Resource)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Subject)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Lesson)
admin.site.register(Notification)