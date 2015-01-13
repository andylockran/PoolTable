from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from PoolScores.forms import MatchInitiateForm

def home(request):

   if request.method =='POST':
   	  form = MatchInitiateForm(request.POST)

   	  if form.is_valid():
   	  	  return HttpResponseRedirect('/league')

   else:
   	  form = MatchInitiateForm()

   context = RequestContext(request,
                           {'request': request,
                            'user': request.user,
                            'form': form,
                            })
   return render_to_response('home.html',
                             context_instance=context)

def score(request):
   context = RequestContext(request,
                           {'request': request,
                            'user': request.user
                            })
   return render_to_response('score.html',
                             context_instance=context)