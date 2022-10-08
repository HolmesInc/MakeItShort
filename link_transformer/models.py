from django.db import models


class URL(models.Model):
    origin_url = models.URLField(unique=True)
    url_hash = models.CharField(max_length=30)


class LinkUser(models.Model):
    url = models.ForeignKey(URL, on_delete=models.DO_NOTHING)
    user_ip = models.CharField(max_length=30)
