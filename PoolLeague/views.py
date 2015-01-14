from django.shortcuts import render_to_response
from django.template.context import RequestContext
from PoolScores.models import Match,UserScore
from django.contrib.auth.models import User
import pprint

# Create your views here.

def leaguetable(request):

   matches = Match.objects.all()
   userList = User.objects.all()
   users = UserScore.objects.order_by('-score')

   pprint.pprint(users)

   context = RequestContext(request,
                           {'request': request,
                            'user': request.user,
                            'users': userList
                            })
   return render_to_response('league.html',
                             context_instance=context
                             )
