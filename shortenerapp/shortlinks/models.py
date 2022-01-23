from django.db import models
from .utils import make_hash
# Create your models here.



class ShortLink(models.Model):
    origin = models.URLField(max_length=1000) #origin url, should not be unique
    hash = models.CharField(null=True,blank=True,unique=True, max_length=7)
    clicks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.pk

    def save(self, *args, **kwargs):
        if not self.pk: # only new created links
            hash = make_hash()
            while ShortLink.objects.filter(hash=hash).exists():
                hash = make_hash()
            self.hash = hash
        super(ShortLink, self).save()

    def increment_clicks(self):
        self.clicks+=1
        self.save()