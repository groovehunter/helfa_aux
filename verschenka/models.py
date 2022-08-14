from django.db import models


class Item(models.Model):
    name  = models.CharField(max_length=100)
    descr = models.TextField(blank=True, verbose_name='Beschreibung')
    added_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return '<a href="/verschenka/item/%d">%s</a>' %(self.id, self.name)


