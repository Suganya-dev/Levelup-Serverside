from django.db import models

class Event(models.Model):

    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    game = models.ForeignKey("Games", on_delete=models.CASCADE)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    date = models.DateField(auto_now=False, auto_now_add=False)

    @property
    def joined(self):
            return self.__joined

    @joined.setter
    def joined(self, value):
            self.__joined = value

