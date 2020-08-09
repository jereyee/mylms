from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .forms import *

from django.contrib.admin import widgets
from django.core.exceptions import ObjectDoesNotExist
from .models import SUBJECTS

from django.utils import timezone

import json

def notification(request):
    return render(request, "lms/notification.html", {
        'notifs': request.user.notifs.all().order_by('-timestamp'),
    })

def assignments(request):
    subjects = request.user.subjects.all()
    homework = Assignment.objects.filter(subject__in=subjects).order_by('-opened_at')

    # handle creation of new assignment
    if request.method == 'POST':

        assignment_form = AssignmentForm(request.POST)
        if assignment_form.is_valid():
            obj = assignment_form.save(commit=False)
            obj.opened_by = request.user
            obj.save()

            # create a notification
            create_notif(users=User.objects.filter(subjects__id=obj.subject.id), 
                text=("<strong>" + request.user.username + "</strong>" + " added a new assignment - " + 
                "<a href='assignments/" + str(obj.id) + "'>" + obj.title + "</a>"))

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('assignments'))

    assignment_form = None

    if request.user.role == 'teacher':
        assignment_form = AssignmentForm(subjects=request.user.subjects.all())

    return render(request, "lms/assignments.html", {
        'assignment_form': assignment_form,
        'assignments': homework,
        'now': timezone.now(),
    })

def submission(request, assignment_id):
    assignment = Assignment.objects.get(pk=assignment_id)

    submission_form = None
    message = ''
    submissions = None
    unsubmitted_students = []

    if request.user.role == 'student':

        try: 
            Submission.objects.get(student=request.user, assignment=assignment)
            message = 'You have submitted this assignment.'
        except ObjectDoesNotExist:
            if timezone.now() > assignment.deadline:
                message = 'The deadline for this assignment has passed.'
            else:
                submission_form = SubmissionForm()

        # Handle file upload
        if request.method == 'POST':
            form = SubmissionForm(request.POST, request.FILES)
            if form.is_valid():
                # create a notification
                create_notif(users=[assignment.opened_by], 
                    text=("<strong>" + request.user.username + "</strong>" + " has handed in " + 
                    "<a href='assignments/" + str(assignment.id) + "'>" + assignment.title + "</a>"))

                newdoc = Submission(
                    doc=request.FILES['doc'], 
                    student=request.user,
                    filename=(request.FILES['doc'].name + ' - ' + request.user.username),
                    assignment=assignment,
                    )
                newdoc.save()

                # Redirect to the document list after POST
                return HttpResponseRedirect(reverse('submission', kwargs={
                    'assignment_id': assignment_id
                }))
            else: 
                print("form not valid")
                print(form.errors)
    
    elif request.user.role == 'teacher':
        # get all the submissions
        submissions = Submission.objects.filter(assignment=assignment).order_by("-timestamp")
        # get all the students
        for student in User.objects.filter(role='student'):
            # check if the student is taking the subject, 
            # and if the student joined before the assignment was posted
            if assignment.subject in student.subjects.all() and student.date_joined < assignment.deadline:
                try: 
                    Submission.objects.get(student=student, assignment=assignment)
                except Submission.DoesNotExist:
                    unsubmitted_students.append(student)

    return render(request, "lms/submission.html", {
        'assign': assignment,
        'submission_form': submission_form,
        'message': message,
        'submissions': submissions,
        'unsubmitted_students': unsubmitted_students,
    })

def lessons(request):
    lesson_form = None

    # handle lesson creation
    if request.method == 'POST':
        lesson_form = LessonForm(request.POST)
        if lesson_form.is_valid():
            obj = lesson_form.save(commit=False)
            obj.teacher = request.user
            obj.save()

            # create a notification
            create_notif(users=User.objects.filter(subjects__id=obj.subject.id), 
                text=("<strong>" + request.user.username + "</strong>" + " added a new lesson to " + 
                obj.subject.name.title() + ": " + 
                "<a href='lessons/" + str(obj.id) + "'>" + obj.title + "</a>"))


            # Redirect to the lesson list after POST
            return HttpResponseRedirect(reverse('lessons'))

    if request.user.role == 'teacher':
        lesson_form = LessonForm(subjects=request.user.subjects.all())

    # Create a dictionary of all the lessons
    video_lessons = {}
    for subj in request.user.subjects.all():
        video_lessons[subj.name] = []
        for obj in Lesson.objects.filter(subject=subj).order_by("-timestamp"):
            video_lessons[subj.name].append(obj)
    
    print(video_lessons)
    return render(request, "lms/lessons.html", {
        'lessons': video_lessons,
        'lesson_form': lesson_form,
    })

def lesson(request, lesson_id):
    video_lesson = Lesson.objects.get(pk=lesson_id)

    return render(request, "lms/lesson.html", {
        'lesson': video_lesson,
    })

def resources(request):

    if request.method == "PUT":
        data = json.loads(request.body)
        
        # check whether the post is eeleted
        if data.get("deleted") is True:
            # Delete resource resource
            try:
                Resource.objects.get(pk=data.get("deleted_id")).delete()
            except Resource.DoesNotExist:
                return JsonResponse({"error": "Resource not found."}, status=404)

        return JsonResponse({
            "deleted": data.get("deleted"),
        }, status=200)

    # Handle file upload
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Resource(
                doc=request.FILES['doc'], 
                uploaded_by=request.user,
                filename=request.FILES['doc'].name,
                subject=Subject.objects.get(pk=request.POST['subject'])
                )
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('resources'))
        else: 
            print("form not valid")
            print(form.errors)
    else:
        form = ResourceForm() # A empty, unbound form

    # Create a dictionary of all the documents
    documents = {}
    for subj in Subject.objects.all():
        if subj in request.user.subjects.all():
            documents[subj.name] = []
            for doc_obj in Resource.objects.filter(subject=subj).order_by("-timestamp"):
                documents[subj.name].append(doc_obj)

    return render(request, "lms/resources.html", {
        "upload_form": form,
        "resources": documents,
    })

def forum(request):
    subjects = request.user.subjects.all()
    posts = None

    # user searching for a forum post
    query = request.GET.get('q')
    if query is not None:
        # find posts with the query
        posts = Post.objects.filter(title__contains=query, subject__in=subjects)
        print(posts)

    return render(request, "lms/forum.html", {
        'subjects': subjects,
        'main': True,
        'posts': posts,
    })

def forum_posts(request, subject):

    if request.method == "POST":
        # saves the new post by the user
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            obj = post_form.save(commit=False)
            obj.subject = Subject.objects.get(name=subject)
            obj.user = request.user
            obj.save()

            # create a notification
            create_notif(users=User.objects.filter(subjects__id=obj.subject.id), 
                text=("<strong>" + request.user.username + "</strong>" + " posted on the " + 
                obj.subject.name.title() + " forum: " + 
                "<a href='forum/" + obj.subject.name + "/" + str(obj.id) + "'>" + obj.title + "</a>"))

            return HttpResponseRedirect(reverse("forum_posts", kwargs={
                'subject': subject
            }))

    # get all posts with this subject
    subj = Subject.objects.get(name=subject)
    posts = Post.objects.filter(subject=subj).order_by("-timestamp")

    form = PostForm()

    return render(request, "lms/forum.html", {
        'subject': subject.title(),
        'main': False,
        'post_form': form,
        'posts': posts,
    })

def post(request, subject, post_id):
    get_post = Post.objects.get(pk=post_id)

    form = CommentForm()

    if request.method == "PUT":
        data = json.loads(request.body)
        
        # check whether the post is edited
        if data.get("content") is not None:
            # Query for requested post
            try:
                check_post = Post.objects.get(user=request.user, pk=post_id)
            except Post.DoesNotExist:
                return JsonResponse({"error": "Post not found."}, status=404)

            check_post.content = data['content']
            check_post.last_modified = timezone.now()

        check_post.save()
        return JsonResponse({
            "content": data['content'],
            "last_modified": check_post.last_modified,
        }, status=200)

    if request.method == "POST":
        # saves the new reply by the user
        reply_form = CommentForm(request.POST)

        if reply_form.is_valid():
            # create a notification
            create_notif(users=[get_post.user], 
                text=("<strong>" + request.user.username + "</strong>" + " replied to your forum post -  " + 
                "<a href='" + request.path + "'>" + get_post.title + "</a>"))

            obj = reply_form.save(commit=False)
            obj.post = Post.objects.get(pk=post_id)
            obj.user = request.user
            obj.save()
            
            return HttpResponseRedirect(reverse("post", kwargs={
                'subject': subject,
                'post_id': post_id,
            }))

    return render(request, "lms/forum_post.html", {
        'subject': subject,
        'post': get_post,
        'replies': Comment.objects.filter(post=get_post).order_by("-timestamp"),
        'comment_form': form,
    })

def create_notif(users, text):
    notif = Notification.objects.create(text=text)
    for person in users:
        person.notifs.add(notif)

def index(request):

    if request.method == "POST":
        # create a notification
        create_notif(users=User.objects.all(), 
            text="<strong>" + request.user.username + "</strong>" + " posted a new update.")

        # saves the new post by the user
        update_form = UpdateForm(request.POST)
        if update_form.is_valid():
            obj = update_form.save(commit=False)
            obj.user = request.user
            obj.save()
            return HttpResponseRedirect(reverse("index"))

    # get all existing updates
    updates = Update.objects.all().order_by("-timestamp")

    form = None
    try:
        if request.user.role == "teacher":
            form = UpdateForm()
    except AttributeError:
        pass

    return render(request, "lms/index.html", {
        "update_form": form,
        "updates": updates,
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            # check if user has been approved by the admin
            if user.approved:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "lms/login.html", {
                "message": "Your account has not yet been approved."
                })

        else:
            return render(request, "lms/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "lms/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "lms/register.html", {
                "message": "Passwords must match.",
                'subjects': SUBJECTS
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            # add subjects
            for subj in Subject.objects.all():
                if subj.name in request.POST:
                    user.subjects.add(subj)
            user.save()
            return render(request, "lms/login.html", {
                "message": "Thank you for registering. Please wait for account approval."
            })
        except IntegrityError:
            return render(request, "lms/register.html", {
                "message": "Username already taken.",
                'subjects': SUBJECTS
            })
        #login(request, user)
        #return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "lms/register.html", {
            'subjects': SUBJECTS
        })
