from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
import os

from .models import Journey, JourneyImage, Like, Comment


def index(request):
    if request.user.is_authenticated:
        journeys = (
            Journey.objects.filter(author=request.user, is_deleted=False) |
            Journey.objects.filter(is_private=False, is_deleted=False)
        )
    else:
        journeys = Journey.objects.filter(is_private=False, is_deleted=False)

    journeys = journeys.distinct().order_by('-created_at')
    return render(request, 'index.html', {'journeys': journeys})


def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully 🎉")
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def add_blog(request):
    if request.method == 'POST':
        journey = Journey.objects.create(
            author=request.user,
            title=request.POST['title'],
            location=request.POST['location'],
            description=request.POST['description'],
            is_private=('is_private' in request.POST),
            song=request.FILES.get('song')
        )

        for img in request.FILES.getlist('images'):
            JourneyImage.objects.create(journey=journey, image=img)

        messages.success(request, "Journey added ❤️")
        return redirect('index')

    return render(request, 'add_blog.html')


@login_required
def edit_journey(request, id):
    journey = get_object_or_404(Journey, id=id, is_deleted=False)

    if journey.author != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        journey.title = request.POST['title']
        journey.location = request.POST['location']
        journey.description = request.POST['description']
        journey.is_private = ('is_private' in request.POST)

        # remove song
        if request.POST.get('remove_song'):
            if journey.song and os.path.isfile(journey.song.path):
                os.remove(journey.song.path)
            journey.song = None

        # replace song
        elif request.FILES.get('song'):
            if journey.song and os.path.isfile(journey.song.path):
                os.remove(journey.song.path)
            journey.song = request.FILES.get('song')

        journey.save()

        for img in request.FILES.getlist('images'):
            JourneyImage.objects.create(journey=journey, image=img)

        messages.success(request, "Journey updated ✨")
        return redirect('blog_detail', id=id)

    return render(request, 'edit_blog.html', {'journey': journey})


def blog_detail(request, id):
    journey = get_object_or_404(Journey, id=id, is_deleted=False)

    if journey.is_private and journey.author != request.user:
        return HttpResponseForbidden("This journey is private 🔒")

    if request.method == 'POST' and request.user.is_authenticated:
        Comment.objects.create(
            journey=journey,
            user=request.user,
            text=request.POST['comment']
        )
        messages.success(request, "Comment added 💬")
        return redirect('blog_detail', id=id)

    return render(request, 'blog_detail.html', {'journey': journey})


@login_required
def like_journey(request, id):
    journey = get_object_or_404(Journey, id=id, is_deleted=False)
    Like.objects.get_or_create(journey=journey, user=request.user)
    return redirect('blog_detail', id=id)


@login_required
def delete_journey(request, id):
    journey = get_object_or_404(Journey, id=id)

    if journey.author != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        journey.is_deleted = True
        journey.save()
        messages.success(request, "Journey deleted 🗑")
        return redirect('index')

    return render(request, 'delete_confirm.html', {'journey': journey})
