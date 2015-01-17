from django.shortcuts import render_to_response
from django.template.context import RequestContext
from PoolScores.models import Match
from django.contrib.auth.models import User
from PoolLeague import services
from datetime import datetime

# Create your views here.

def leaguetable(request):
  league = services.getLeague(datetime.now())
  context = RequestContext(request, {'request': request,'user': request.user,'league': league})
  return render_to_response('league.html',context_instance=context)
