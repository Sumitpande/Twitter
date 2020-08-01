from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse

from .models import *
import json
from django.http import JsonResponse
from django.forms.models import model_to_dict
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator



def index(request):
    if request.method == "POST": 
        text = request.POST["text"].strip()
        
        tweet = Tweet.objects.create(text=text,user=request.user)
        #tweet.save()
        if(tweet):print(f'text-{text}')

    tweets = Tweet.objects.all().order_by("-date_created")
    
    paginator = Paginator(tweets, 10) # Show 10 posts per page.

    page_number = request.GET.get('page')
    tweets = paginator.get_page(page_number)
    
    
    return render(request, "network/index.html", {
        
        'tweets':tweets

    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")



@csrf_exempt
def editpost(request,id):
    
    try:
        tweet = Tweet.objects.get(user=request.user, pk=id)
    except Tweet.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("text") is not None:
            tweet.text = data["text"]
            # tweet.date_updated = datetime.datetime.now()
        
        tweet.save()
        return HttpResponse(status=204)

    
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


    return JsonResponse({
            "message": "Post Edited"
        }, status=201)


def profileView(request,uid):
    
    tweets = Tweet.objects.filter(user = uid).order_by('-date_created')
    followers = Follow.objects.filter(following=uid)
    followings = Follow.objects.filter(follower=uid)
    y = [x.follower.id for x in followers]
    print(f'yes {y}')
    user = User.objects.get(id=uid)
    for t in tweets:
        user = t.user

    paginator = Paginator(tweets, 10) # Show 10 posts per page.

    page_number = request.GET.get('page')
    tweets = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        'tweets':tweets,
        'username':user,
        'followers':followers,
        'followings':followings,
        'y':y
    })

def followingView(request):
    t = Tweet.objects.all().order_by('-date_created')
    follows = Follow.objects.filter(follower=request.user)
    tweets=[]
    for p in t:
        for f in follows:
            if f.following == p.user:
                tweets.append(p)

    paginator = Paginator(tweets, 5) # Show 10 posts per page.

    page_number = request.GET.get('page')
    tweets = paginator.get_page(page_number)

    if not follows:
        return render(request, "network/index.html", {
        'tweets':tweets,
        'msg':True
        })


    return render(request, "network/index.html", {
        'tweets':tweets
    })


@csrf_exempt
def likepost(request,id):
    tweet = Tweet.objects.get(pk=id)
    if request.method == 'GET':
        if request.user in tweet.likes.all():
            tweet.likes.remove(request.user)
            like = Likes.objects.get(tweet=tweet,user=request.user)
            like.delete()
        else:
            like = Likes.objects.get_or_create(tweet=tweet, user=request.user)
            
            tweet.likes.add(request.user)
            tweet.save()

    return JsonResponse(tweet.serialize(), safe=False)
    


@csrf_exempt
def follow(request, username):
    if request.method == 'GET':
        user_profile = get_object_or_404(User, username=username)
        is_follows = Follow.objects.filter(follower=request.user,following=user_profile)
        

        if is_follows:
            is_follows.delete()
        else:
            follow = Follow.objects.get_or_create(follower=request.user,following=user_profile)
            


        flrs = Follow.objects.filter(following=user_profile).count()
        foling = Follow.objects.filter(follower=user_profile).count()
        
    return JsonResponse({"followers":flrs,"followings":foling,}, safe=False)