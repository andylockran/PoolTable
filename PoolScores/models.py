from __future__ import division
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from datetime import datetime
from pprint import pprint


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
	winner=models.ForeignKey(User,related_name="winningplayer",blank="True",null="True")
	ballsLeft = models.IntegerField(choices=BALLS_LEFT_CHOICES,blank="True",null="True")
	points = models.IntegerField(blank="True",null="True")
	def __unicode__(self):
		title = str(self.breakPlayer) + str(self.challenger)
		return title

	def getLeague(self, *args, **kwargs):
		league = {}
		pos = 0
		compare = 0
		playerList = UserScore.objects.order_by('-date').distinct
		"""@Todo make sure this list only gets most recent score for each player"""
		for player in playerList:
			league[player.user] = {}
			if compare != player.score:
				pos=pos+1
				compare = player.score
			league[player.user]['pos'] = pos
			league[player.user]['score'] = player.score

		return league	

	def getPositionalDifference(self):

		positions = self.getLeague()
		
		diff =  positions[self.breakPlayer]['pos'] - positions[self.challenger]['pos']

		if diff < -10:
			diff = -10

		if diff > 10:
			diff = 10

		return diff

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

			if self.ballsLeft < 2:
				multiplier = 1
			elif self.ballsLeft > 2:
				multiplier = 1.5
			elif self.ballsLeft > 4:
				multiplier = 2

			print multiplier

			#End of Multiplier Calculation
			print "Difference"
			difference = self.getPositionalDifference()
			print difference
			#if self.foulOnBlack == "True":


			if self.winner == self.breakPlayer:
			   winplayer = UserScore.objects.get(user=self.breakPlayer)
			   loseplayer = UserScore.objects.get(user=self.challenger)
			   pointscalc = self.point_calc(difference -2)
			   points = pointscalc * multiplier
			   self.points = points
			   winpoints = winplayer.score + points
			   losepoints = loseplayer.score - points
			   UserScore.objects.get_or_create(user=self.breakPlayer,score=winpoints,date=self.date,match=self)
			   UserScore.objects.get_or_create(user=self.challenger,score=losepoints,date=self.date,match=self)
			else:
			   winplayer = UserScore.objects.get(user=self.challenger)
			   loseplayer= UserScore.objects.get(user=self.breakPlayer)
			   pointscalc = self.point_calc(difference +2)
			   points = pointscalc * multiplier
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

class Score(models.Model):
	match = models.ForeignKey(Match)
	score = models.IntegerField()
	date = models.DateTimeField(blank="False")
	def __unicode__(self):
		return str(self.match)

class UserScore(models.Model):
	user = models.ForeignKey(User)
	score = models.IntegerField()
	date = models.DateTimeField()
	match = models.ForeignKey(Match,null="True",blank="True")
	def __unicode__(self):
		return str(self.user)

class MatchAdmin(admin.ModelAdmin):
	pass

class ScoreAdmin(admin.ModelAdmin):
	pass	

class UserScoreAdmin(admin.ModelAdmin):
	pass	

admin.site.register(Match, MatchAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(UserScore, UserScoreAdmin)





