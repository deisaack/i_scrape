from django.db import models


class Post(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    shortcode = models.CharField(max_length=20, null=True, blank=True)
    comments = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(null=True, blank=True)
    owner_id = models.PositiveIntegerField(null=True, blank=True)
    tag = models.CharField(null=True, blank=True, max_length=20)
    other_tags = models.CharField(null=True, blank=True, max_length=200)
    caption = models.TextField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

