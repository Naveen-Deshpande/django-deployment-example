from django.db import models
# import the timezone module from the utils
from django.utils import timezone
from django.urls import reverse

# Create your models here.
# create a post model that saves the posts on the blog back to the model
class Post(models.Model):
    '''
    post model with fields author,title,text,create_date,published_date
    returns the title of the post
    '''
    # author is directly linked to the authorisation User, someone who can
    # have control over the posts, so that it can be saved as drafts and then published
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    # creted_date will be a datetimefield which basically uses the current
    # timezone of the project, you can check the settings.py for the timezone
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)

    # method to save the published_date since it can be blank or null
    # once published we can save the current time
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # method to approve the comments on the blog
    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    # get_absolute_url is the method which redirects the user once the user is
    # finished posting the on the blog, this tells django to return to the post
    # detail page with the primary key of just created post
    def get_absolute_url(self):
        return reverse('post_detail',kwargs={'pk':self.pk})

    # method for string represntation ofthe class
    def __str__(self):
        return self.title


# create a comments model to store the comments posted on the blog
class Comment(models.Model):
    '''
    comments model with fields posts,author,text,created_date,approved_comments
    returns text
    '''
    # post is the foreign key that directly connects to the post model
    post = models.ForeignKey('Blog.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=256)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    # method to approve the comments on the blog and save them
    def approve(self):
        self.approved_comment = True
        self.save()

    # after commenting on the posts the user is redirected to the home page of
    # the blog
    def get_absolute_url(self):
        return reverse('post_list')

    # string represntation of the comments model
    def __str__(self):
        return self.text
