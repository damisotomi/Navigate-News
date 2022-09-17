from django.db import models
from django.urls import reverse

# Create your models here.


class News(models.Model):
    item_id = models.CharField(max_length=255, blank=True, null=True)
    author = models.TextField(null=True, blank=True, help_text='(optional)')
    title = models.TextField(null=True, blank=True, help_text='(optional)')
    descendants = models.IntegerField(
        help_text="Total Comment count", null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)

    TYPE_OPTION_STORY = 'story'
    TYPE_OPTION_COMMENT = 'comment'
    TYPE_OPTION_POLL = 'poll'
    TYPE_OPTION_JOB = 'job'
    TYPE_OPTION_POLL_OPTION = 'pollopt'
    TYPE_OPTION_NO_CATEGORY = 'other'

    TYPE_OPTION_CHIOCES = [
        (TYPE_OPTION_STORY, 'Story'),
        (TYPE_OPTION_COMMENT, 'Comment'),
        (TYPE_OPTION_POLL, 'Poll'),
        (TYPE_OPTION_JOB, 'Job'),
        (TYPE_OPTION_POLL_OPTION, 'Poll option'),
        (TYPE_OPTION_NO_CATEGORY, 'other')
    ]
    type = models.CharField(
        max_length=255, help_text="Enter either one of Job, Story, Comment, Poll or Poll option", choices=TYPE_OPTION_CHIOCES, default=TYPE_OPTION_STORY)
    text = models.TextField(null=True, blank=True,
                            help_text="The comment, story or poll text.(optional)")
    url = models.URLField(null=True, blank=True, help_text='(optional)')
    # this is to record the time when we update/edit the products
    last_update = models.DateTimeField(auto_now=True)
    # this is to record the time when we create a new instance
    date_created = models.DateTimeField(auto_now_add=True)
    classification = models.CharField(default='HackerNews', max_length=255)

    def __str__(self) -> str:
        """string for representing the Model Object(in admin site)"""
        return self.title

    def get_absolute_url(self):
        '''Returns the Url  to access a detail record for this News Item'''
        return reverse("news_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ['-id']


class Comment(models.Model):
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name="comments")
    item_id = models.CharField(max_length=255, blank=True, null=True)
    author = models.TextField(null=True, blank=True,help_text='Name of commenter')
    comment = models.TextField(null=True, blank=True, help_text="Write your comment here")
    type = models.CharField(max_length=255,default='comment')
    classification = models.CharField(max_length=255,default='HackerNews comment')
    
    class Meta:
        ordering = ['-id']

