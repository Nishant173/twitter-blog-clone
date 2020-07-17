""" Run this code in the shell to generate random posts """

import random
from account.models import Account
from blog.models import Post


def add_random_post():
    low, high = 1, 1000
    authors = Account.objects.all()
    post_obj = Post.objects.create(author=random.choice(authors),
                                   title=f"Title {random.randint(low, high)}",
                                   content=f"Content {random.randint(low, high)}")
    post_obj.save()


for _ in range(25):
    add_random_post()