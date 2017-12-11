


from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from django.urls import reverse

# Create your models here.
Game_STATUS_Choices=(
    ('F','first player to move'),
    ('S','second to move'),
    ('w','first player wins'),
    ('l','second player wins'),
    ('d','draw')
)
class GameQuerySet(models.QuerySet):
    def games_for_user(self,user):
        return self.filter(
            Q(first_player=user)|Q(second_player=user)
        )
    def active(self):
        return self.filter(
        Q(status='F')|Q(status='s')
        )
class Game(models.Model):
    first_player=models.ForeignKey(User,related_name="games_first_player")
    second_player=models.ForeignKey(User,related_name="games_second_player")
    start_time=models.DateTimeField(auto_now_add=True)
    last_active=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=1,default='F',choices=Game_STATUS_Choices)

    objects=GameQuerySet.as_manager()    #make this as manger in any view 

    def get_absolute_url(self):
        return reverse('gameplay_detail',args=[self.id])


    def __str__(self):
        return "{0} vs {1}".format(
            self.first_player,self.second_player
        )

class Move(models.Model):
    x=models.IntegerField()
    y=models.IntegerField()
    comment=models.CharField(max_length=300,blank=True)
    by_first_player=models.BooleanField()

    game=models.ForeignKey(Game,on_delete=models.CASCADE)