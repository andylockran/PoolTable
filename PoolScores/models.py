from __future__ import division
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from datetime import datetime

from PoolLeague import services

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
	breakPlayer = models.ForeignKey(User, related_name="breakPlayer", null="True")
	challenger = models.ForeignKey(User, related_name="challenger", null="True")
	createdBy = models.ForeignKey(User,related_name="matchAdministrator", null="True")
	date = models.DateTimeField()
	foulOnBlack = models.NullBooleanField(blank="True",null="True")
	winner=models.ForeignKey(User,related_name="winningplayer",blank="True",null="True")
	ballsLeft = models.IntegerField(choices=BALLS_LEFT_CHOICES,blank="True",null="True")
	points = models.FloatField(blank="True",null="True")
	
	def __unicode__(self):
		title = str(self.breakPlayer) + str(self.challenger)
		return title

	def initialisePlayers(self):
		#Initialise Players in League
		if not UserScore.objects.filter(user=self.breakPlayer):
			UserScore.objects.create(user=self.breakPlayer,score=40,date=self.date)
			print 'Break Player Initialised'
		
		if not UserScore.objects.filter(user=self.challenger):
			UserScore.objects.create(user=self.challenger,score=40,date=self.date)
			print 'Challenge Player Initialised'

	def point_calc(self,diff):
		x = diff/10
		x = x + 1
		return x

	def calc_score(self, *args, **kwargs):
		"""This function calculates the score"""
		
		self.initialisePlayers()
		print "Calculating score"
		if not self.points:
		
			#Multiplier Calculation
			print "Balls Left: %d\n" % self.ballsLeft;
			multiplier = self.ballsLeft / 2
			print "Multiplier: %f\n" % multiplier
			#End of Multiplier Calculation
			bp = str(self.breakPlayer)
			cp = str(self.challenger)
			difference = services.getPositionalDifference(self.date,bp,cp)
			print "Initial Difference: %f\n" % difference
			#if self.foulOnBlack == "True":

			if self.winner == self.breakPlayer:
			   winplayer = UserScore.objects.filter(user=self.breakPlayer).order_by('-date')[0]
			   loseplayer = UserScore.objects.filter(user=self.challenger).order_by('-date')[0]
			   weightedDifference = difference - 2
			   print "Weighted Difference %f" % weightedDifference
			   pointscalc = self.point_calc(weightedDifference)
			   print "Base Points: %f" % pointscalc
			   points = pointscalc * multiplier
			   print "Calculated Points: %f" % points
			   self.points = points
			   winpoints = winplayer.score + points
			   losepoints = loseplayer.score - points
			   UserScore.objects.get_or_create(user=self.breakPlayer,score=winpoints,date=self.date,match=self)
			   UserScore.objects.get_or_create(user=self.challenger,score=losepoints,date=self.date,match=self)
			else:
			   winplayer = UserScore.objects.filter(user=self.challenger).order_by('-date')[0]
			   loseplayer = UserScore.objects.filter(user=self.breakPlayer).order_by('-date')[0]
			   weightedDifference = difference + 2
			   print "Weighted Difference %f" % weightedDifference
			   pointscalc = self.point_calc(weightedDifference)
			   print "Base Points: %f" % pointscalc
			   points = pointscalc * multiplier
			   print "Calculated Points: %f" % points
			   self.points = points
			   winpoints = winplayer.score + points
			   losepoints = loseplayer.score - points
			   UserScore.objects.get_or_create(user=self.challenger,score=winpoints,date=self.date,match=self)
			   UserScore.objects.get_or_create(user=self.breakPlayer,score=losepoints,date=self.date,match=self)



	def save(self, *args, **kwargs):
		"""
		http://fr.wikipedia.org/wiki/Classement_World_Rugby_des_%C3%A9quipes_nationales_de_rugby_%C3%A0_XV#Calcul
		"""
		if self.winner:
			self.calc_score()
			
		super(Match, self).save(*args,**kwargs)

	class Meta:
		verbose_name_plural = "Matches"

class UserScore(models.Model):
	user = models.ForeignKey(User)
	score = models.FloatField()
	date = models.DateTimeField()
	match = models.ForeignKey(Match,null="True",blank="True")
	def __unicode__(self):
		return str(self.user)

class MatchAdmin(admin.ModelAdmin):
	list_display= ('__unicode__','date','winner','points')

class UserScoreAdmin(admin.ModelAdmin):
	list_display=('__unicode__','date','score')


admin.site.register(Match, MatchAdmin)
admin.site.register(UserScore, UserScoreAdmin)





