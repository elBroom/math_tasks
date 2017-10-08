from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(null=True)
    author = models.ForeignKey('auth.User')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title
