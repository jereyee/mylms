from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = [
    ('teacher', 'Teacher'),
    ('student', 'Student'),
]

SUBJECTS = [
    ('chemistry', 'Chemistry'),
    ('physics', 'Physics'),
    ('math', 'Math'),
    ('economics', 'Economics'),
    ('english', 'English'),
    ('programming', 'Programming'),
    ('history', 'History'),
]

class Subject(models.Model):
    name = models.CharField(max_length=16, choices=SUBJECTS, default='chemistry')
    
    def __str__(self):
        return f"{self.name.title()}"

class Notification(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=256, null=True)

class User(AbstractUser):
    role = models.CharField(max_length=32, choices=ROLES, default='student')
    approved = models.BooleanField(default=None, null=True)
    subjects = models.ManyToManyField(Subject, blank=True, related_name="subjects")
    notifs = models.ManyToManyField(Notification, blank=True, related_name="notif")


class Update(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    content = models.TextField(verbose_name=u"", default="", max_length=1028)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Update by {self.user}"

class Resource(models.Model):
    #subject = models.CharField(max_length=16, choices=SUBJECTS, default='ch')
    subject = models.ForeignKey(Subject, verbose_name=u"", null=False, default="chemistry", on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    directory = 'resources/'
    doc = models.FileField(verbose_name=u"", upload_to=directory)
    filename = models.CharField(max_length=128, default="filename")

class Assignment(models.Model):
    subject = models.ForeignKey(Subject, null=False, default=1, on_delete=models.CASCADE)
    opened_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    opened_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=False)
    title = models.CharField(max_length=128, null=False, default="Assignment")
    description = models.CharField(max_length=512, null=True)

    def __str__(self):
        return f"{self.title}"

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, null=True, on_delete=models.CASCADE)
    student = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    directory = 'submissions/'
    doc = models.FileField(verbose_name=u"", upload_to=directory, null=True)
    filename = models.CharField(max_length=128, default="filename-student")

class Post(models.Model):
    subject = models.ForeignKey(Subject, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(verbose_name=u"Post Title", default="", max_length=64)
    content = models.TextField(verbose_name=u"Post Content", default="", max_length=1028)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.user} - {self.title}"

class Comment(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    content = models.TextField(verbose_name=u"", default="", max_length=1028)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.post.title}"

class Lesson(models.Model):
    subject = models.ForeignKey(Subject, null=False, on_delete=models.CASCADE, default=1)
    teacher = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128, null=False, default="Lesson")
    url = models.CharField(verbose_name=u"Lesson URL (YouTube)", max_length=256, null=False, default="")

    def __str__(self):
        return f"{self.title} by {self.teacher}"

    def get_embed_url(self):
        return self.url.replace("watch?v=", "embed/")

    