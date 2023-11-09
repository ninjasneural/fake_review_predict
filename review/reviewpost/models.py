from django.db import models

# Create your models here.
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    review = models.CharField(max_length=200)
    user_id = models.IntegerField()
    status = models.CharField(max_length=20)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'review'

