from django.db import models
from .validators import validate_score

class Review(models.Model):
    title = models.CharField(max_length=200)
    writer = models.CharField(max_length=100)
    pub_date = models.DateTimeField()
    body = models.TextField()
    score = models.FloatField(default=3, null=True, validators=[validate_score])

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]