from django.db import models


class Booking(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=250)
    phone_number = models.CharField(max_length=25)
    people = models.PositiveIntegerField(default=1)
    date = models.DateField()
    time = models.TimeField()

    class occasion(models.TextChoices):
        NONE = "None"
        BIRTHDAY = "Birthday"
        ANNIVERSARY = "Anniversary"
        ENGAGEMENT = "Engagement"
        OTHER = "Other"
    class seating_preferences(models.TextChoices):
        NONE = "None"
        INDOORS = "Indoors"
        PATIO = "Outdoor (Patio)"
        SIDEWALK = "Outdoor (Sidewalk)"

    additional_comments = models.TextField(default='Optional', max_length=3000)

    def __str__(self):
        return str(self.date) + ":" + str(self.time)
class Menu(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField()

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menu Items'

    def __str__(self) -> str:
        return f'{self.title} : {str(self.price)}'