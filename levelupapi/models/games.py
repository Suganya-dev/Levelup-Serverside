from django.db import models

class Games(models.Model):

    title= models.CharField(max_length=50)
    maker=models.CharField(max_length=20)
    gametype= models.ForeignKey("GameType",on_delete=models.CASCADE)
    number_of_players= models.IntegerField()
    gamer= models.ForeignKey("Gamer",on_delete=models.CASCADE)
    skill_level= models.IntegerField()