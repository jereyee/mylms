
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("notif", views.notification, name="notification"),
    path("lessons", views.lessons, name="lessons"),
    path("lessons/<int:lesson_id>", views.lesson, name="lesson"),
    path("resources", views.resources, name="resources"),
    path("assignments", views.assignments, name="assignments"),
    path("assignments/<int:assignment_id>", views.submission, name="submission"),
    path("forum", views.forum, name="forum"),
    path("forum/<str:subject>", views.forum_posts, name="forum_posts"),
    path("forum/<str:subject>/<int:post_id>", views.post, name="post"),
]
