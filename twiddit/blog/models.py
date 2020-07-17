from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
# from django.utils import timezone
from . import utils
from account.models import Account


class Post(models.Model):
    author = models.ForeignKey(to=Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    upvotes = models.ManyToManyField(to=Account, related_name='upvotes', blank=True)
    downvotes = models.ManyToManyField(to=Account, related_name='downvotes', blank=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    
    class Meta:
        ordering = ['-date_posted']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse(viewname='post-detail', kwargs={'slug': self.slug})
    
    @property
    def total_upvotes(self):
        return self.upvotes.count()
    
    @property
    def total_downvotes(self):
        return self.downvotes.count()


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = utils.unique_slug_generator(instance=instance)

pre_save.connect(receiver=slug_generator, sender=Post)


class Comment(models.Model):
    author = models.ForeignKey(to=Account, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date_posted']
    
    def __str__(self):
        return self.content
    
    def get_absolute_url(self):
        return reverse(viewname='post-detail', kwargs={'slug': self.slug})