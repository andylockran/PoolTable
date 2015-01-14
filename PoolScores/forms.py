from django.forms import ModelForm
from PoolScores.models import Match

class MatchInitiateForm(ModelForm):
	class Meta:
		model = Match
		fields = ['breakPlayer','challenger','date']