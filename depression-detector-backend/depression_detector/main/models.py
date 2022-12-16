from django.db import models
from django.utils.translation import gettext_lazy


# Create your models here.
class Model(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.TextField()
    date_of_birth = models.DateField()
    depression_detection_result = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    class SexChoices(models.TextChoices):
        MALE = 'M', gettext_lazy('MALE')
        FEMALE = 'F', gettext_lazy('FEMALE'),
        OTHER = 'O', gettext_lazy('OTHER')

    sex = models.CharField(
        max_length=10,
        choices=SexChoices.choices
    )
