from django.db import models

# Create your models here.
class Content(models.Model):
    title = models.CharField(max_length=50)
    module = models.TextField()
    students = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(null=True, blank=True,default=False)

    def __repr__(self):
        return f'<[{self.id}] {self.title} - {self.module}>'