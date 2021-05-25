from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from django.urls import reverse
from django.utils.text import slugify


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    username_slug = models.SlugField(blank=True)

    # the user's overall rating, given by the rating on all of their todolists
    rating = models.PositiveIntegerField(default=0)

    # list of all the lists that this user has rated
    rated_goals = models.ManyToManyField('Goal', blank=True)

    def save(self, *args, **kwargs):
        self.username_slug = slugify(super(User, self).username)
        super(User, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('goal:user-detail', kwargs={'username_slug': self.username_slug})


class Goal(models.Model):
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    PUBLICITY_CHOICES = (
        ('p', 'public'),
        ('pr', 'private'),
    )
    publicity = models.CharField(
        max_length=7,
        choices=PUBLICITY_CHOICES,
        default='pr',
        help_text='Do you want this goal to be available to the public?',
    )
    description = models.CharField(max_length=300, null=True, blank=True)
    upvotes = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    goal_slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.goal_slug = slugify(self.title)
        super(Goal, self).save(*args, **kwargs)

    def get_absolute_url(self):
        user = self.owner
        username_slug = user.username_slug
        return reverse('goal:goal-detail', kwargs={
            'goal_slug': self.goal_slug,
            'pk': self.id,
            'username_slug': username_slug,
        })

    def __str__(self):
        return f"{self.title}, by {self.owner}"


class Category(models.Model):
    name = models.CharField(max_length=50)
    goals = models.ManyToManyField(Goal)

    category_slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.category_slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('goal:category', args=[str(self.category_slug)])


class Comment(models.Model):
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    text = models.TextField(
        validators=[MinLengthValidator(
            3, "Comment must be greater than 3 characters")],
        blank=True,
        null=True,
    )
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}, on goal: {self.goal}"

    def get_absolute_url(self):
        return self.goal.get_absolute_url()
