from django.db import models


class SearchCity(models.Model):
    name = models.CharField(max_length=256)
    searchs = models.IntegerField(default=0)

    def serialize(self):
        return {
            'name': self.name,
            'searchs': self.searchs
        }
