from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass

class Tweet(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="tweets")
    text = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now=True)
    # date_updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField('User', default=None, blank=True, related_name='tweet_likes')

    # def get_likes(self):
    #     return "\n".join([p for p in self.likes.all()])

    def serialize(self):
        return {
            "id": self.id,
            "likes": self.likes.all().count(),
            "likeduser": [x.id for x in self.likes.all() ],
            "text": self.text,
            "user": self.user.username,
            "date_created": self.date_created.strftime("%b %Od %Y, %I:%M %p")
            
            
        }
    
    def __str__(self):
        return f"{self.user}'s Tweet on {self.date_created}"


class Follow(models.Model):
    following = models.ForeignKey("User", on_delete=models.CASCADE , related_name="following")
    follower = models.ForeignKey("User", on_delete=models.CASCADE , related_name="follower")
    # follow_time = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
            "id": self.id,
            "followers": self.follower,
            "following": self.following
            
            
        }


class Likes(models.Model):
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE, related_name="postlikes")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="postlikes")
    #date_created = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
            "id": self.id,
            "likes": self.tweet,
            "user": self.user,
            "body": self.body
            
        }
    
    def __str__(self):
        return f"{self.user} Like"
    


class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="comments")
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE, related_name="comments")

    content = models.TextField(max_length=2000)
    date_created = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "tweet": self.tweet,
            "content": self.content,
            "date_created": self.date_created.strftime("%b %Od %Y, %I:%M %p")
            
        }

    def __str__(self):
        return self.content

    
