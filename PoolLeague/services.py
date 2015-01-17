from __future__ import division
import operator
from datetime import datetime


def getLeague(date):
	from PoolScores.models import UserScore
	from django.contrib.auth.models import User
	league = {}
	playerList = User.objects.all()
	"""@Todo make sure this list only gets most recent score for each player"""
	for player in playerList:
		pos = 0
		try:
			score = UserScore.objects.filter(user=player).order_by('-date')[0].score
		except:
			if IndexError:
				UserScore.objects.create(user=player,score=40,date=datetime.now())
		league[player.username] = [score,pos]

	sorted_league = sorted(league.items(), key=operator.itemgetter(1))

	sorted_league.reverse()

	position = 0
	prevscore = 0
	for key,value in sorted_league:
		if value[0] != prevscore:
			position = position+1
			prevscore = value[0]
		value[1] = position


	return sorted_league

def getPositionalDifference(date,breakPlayer,challenger):
	
	from PoolScores.models import UserScore
	positions = getLeague(date)
	breakPos=0
	challengePos=0

	for key,value in positions:

		if key == str(breakPlayer):
			breakPos = value[1]
			print "Break Pos: %d" % breakPos
		if key == challenger:
			challengePos = value[1]
			print "Challenge Pos: %d" % challengePos


	diff =  breakPos - challengePos

	if diff < -10:
		diff = -10

	if diff > 10:
		diff = 10

	return diff