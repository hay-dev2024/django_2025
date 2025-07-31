from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_absolute_url(self):
        return f"/library/{self.pk}/"  # pk는 primary key로, 각 게시글을 고유하게 식별하는 값