from django.db import models

class Software(models.Model):
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255, blank=True, null=True)
    team_size = models.CharField(max_length=255, blank=True, null=True)
    platform = models.CharField(max_length=255, blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    price = models.CharField(max_length=50, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'software'

    def __str__(self):
        return self.name
