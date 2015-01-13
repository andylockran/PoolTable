from django.shortcuts import render_to_response
from django.template.context import RequestContext
from PoolScores.models import Match,UserScore
from django.contrib.auth.models import User

# Create your views here.

def home(request):
   users = UserScore.objects.order_by('-score')
   context = RequestContext(request,
                           {'request': request,
                            'user': request.user,
                            'users': users
                            })
   return render_to_response('league.html',
                             context_instance=context
                             )


