from django.db import models


class URL(models.Model):
    origin_url = models.URLField(unique=True)


class User(models.Model):
    user_hash = models.CharField(max_length=30)


class UserLink(models.Model):
    url_id = models.ForeignKey(URL, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    short_url = models.CharField(max_length=30, unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['url_id', 'user_id', 'short_url'], name='unique user link record'),
            models.UniqueConstraint(fields=['url_id', 'user_id'], name='unique user link'),
        ]


class LinkClick(models.Model):
    user_link = models.ForeignKey(UserLink, on_delete=models.CASCADE)
