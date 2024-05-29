from django.db import models


class Category(models.Model):
    title = models.CharField( max_length=200)
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField( max_length=200)
    text = models.TextField()
    img = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    is_active = models.BooleanField(default=False)
    explanation = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='children')
    date = models.DateTimeField(auto_now=True)
    text = models.TextField()



