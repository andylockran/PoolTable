from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.models import User
from PoolScores.models import Match,UserScore
from rest_framework import routers, serializers, viewsets

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Match
        fields = ('breakPlayer','challenger','createdBy','date','foulOnBlack','winner','ballsLeft')

class MatchViewSet(viewsets.ModelViewSet):
        queryset = Match.objects.order_by('-date')
        serializer_class = MatchSerializer

class UserScoreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserScore
        fields = ('user','score','date','match')

class UserScoreViewSet(viewsets.ModelViewSet):
        queryset = UserScore.objects.order_by('-date')
        serializer_class = UserScoreSerializer


router = routers.DefaultRouter()
router.register(r'matches', MatchViewSet)
router.register(r'users', UserViewSet)
router.register(r'scores', UserScoreViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PoolTable.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'PoolScores.views.home', name='home'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^score/$', 'PoolScores.views.score', name='score'),
    url(r'^results/$', 'PoolScores.views.results', name='results'),
    url(r'^league/', include('PoolLeague.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^admin/', include(admin.site.urls)),
)
