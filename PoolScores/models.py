from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from datetime import datetime

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

PLAYERS = (
	('breakPlayer',"Break Player"),
	('challenger', "Challenger"),
	)

class Match(models.Model):
	breakPlayer = models.ForeignKey(User, related_name="breakPlayer", null="True")
	challenger = models.ForeignKey(User, related_name="challenger", null="True")
	createdBy = models.ForeignKey(User,related_name="matchAdministrator", null="True")
	date = models.DateTimeField()
	foulOnBlack = models.NullBooleanField(blank="True",null="True")
	winner=models.CharField(choices=PLAYERS,blank="True",null="True")
	ballsLeft = models.IntegerField(choices=BALLS_LEFT_CHOICES,blank="True",null="True")
	def __unicode__(self):
		title = str(self.breakPlayer) + str(self.challenger)
		return title

	def save(self, *args, **kwargs):
		"""This needs to work out base score,
		then work out the players positional different
		then work out the final score.

		D = The positional difference should be calculated, up to a maximum of 10.

		http://fr.wikipedia.org/wiki/Classement_World_Rugby_des_%C3%A9quipes_nationales_de_rugby_%C3%A0_XV#Calcul

		Based on the IRB rankings:
		1 for 2 balls or less,
		1.5 for 3-5 balls, and
		2 for 6-7 balls.




		"""
		if self.ballsLeft < 2:
			points = 1
		elif self.ballsLeft > 2:
			points = 1.5
		else self.ballsLeft > 4:
			points = 2
		

		Score.objects.get_or_create(match=self,score=points,date=datetime.now())
			
		super(Match, self).save(*args,**kwargs)

	class Meta:
		verbose_name_plural = "Matches"

class Score(models.Model):
	match= models.ForeignKey(Match)
	score = models.IntegerField()
	date = models.DateTimeField(blank="False")
	def __unicode__(self):
		return str(self.user)

class MatchAdmin(admin.ModelAdmin):
	pass


class UserScoreAdmin(admin.ModelAdmin):
	pass	

admin.site.register(Match, MatchAdmin)
admin.site.register(UserScore, UserScoreAdmin)
