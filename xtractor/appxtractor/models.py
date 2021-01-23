from django.db import models

# Create your models here.
class Section(models.Model):
    title = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='chosen_sections/images/', null=True, blank=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)