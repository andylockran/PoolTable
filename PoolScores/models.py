from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.

BALLS_LEFT_CHOICES = (
	(0,"0"),
	(1,"1"),
	(2,"2"),
	(3,"3"),
	(4,"4"),
	(5,"5"),
	(6,"6"),
	(7,"7"),
)

class Match(models.Model):
	breakplayer = models.ForeignKey(User, related_name="breakplayer", null="True")
	challenger = models.ForeignKey(User, related_name="challenger", null="True")
	date = models.DateTimeField()
	blackPottedPrematurelyBy = models.ForeignKey(User,related_name="blackpotter", null="True", blank="True")
	winner=models.ForeignKey(User,related_name="Winner",null="True", blank="True")
	ballsLeft = models.IntegerField(choices=BALLS_LEFT_CHOICES,blank="True",null="True")
	approvedB = models.NullBooleanField(null="True", blank="True")
	approvedC = models.NullBooleanField(null="True", blank="True")
	def __unicode__(self):
		title = str(self.breakplayer) + str(self.challenger)
		return title
	class Meta:
		verbose_name_plural = "Matches"

class UserScore(models.Model):
	user = models.OneToOneField(User, unique="True")
	score = models.IntegerField()
	def __unicode__(self):
		return str(self.user)

class MatchAdmin(admin.ModelAdmin):
	pass

class UserScoreAdmin(admin.ModelAdmin):
	pass	

admin.site.register(Match, MatchAdmin)
admin.site.register(UserScore, UserScoreAdmin)
