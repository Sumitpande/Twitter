from django.contrib import admin
from.models import*
# Register your models here.
class TweetAdmin(admin.ModelAdmin):
    
    list_display = ("id", "user","text", "date_created")
    list_editable = ("user", "text")

class FollowAdmin(admin.ModelAdmin):
    
    list_display = ("id","following","follower" )
    list_editable = ("following","follower")


admin.site.register(User)
admin.site.register(Tweet, TweetAdmin)
admin.site.register(Follow,FollowAdmin)
admin.site.register(Likes)
