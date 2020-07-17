from django.db import models
from PIL import Image
from account.models import Account


class Profile(models.Model):
    user = models.OneToOneField(to=Account, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username} Profile"
    
    def save(self, *args, **kwargs):
        """ Saving profile picture after resizing it """
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Follower(models.Model):
    follower = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name='followers')
    
    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} follows {self.following}"
    
    @property
    def get_follower(self):
        return self.follower # Works on single object, not queryset
    
    @property
    def get_following(self):
        return self.following # Works on single object, not queryset