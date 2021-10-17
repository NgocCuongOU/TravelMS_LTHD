from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField


class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')

class ModelBase(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Post(ModelBase):
    class Meta:
        unique_together = ("title", "category")
        ordering = ["id"]


    title = models.CharField(max_length=255, null=False)
    content = RichTextField(null=False)
    description = models.TextField(max_length=255, null=False, default=None)
    image = models.ImageField(upload_to='posts/%Y/%m', default=None, )
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, related_name='post',on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title

class PostView(ModelBase):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
    views = models.IntegerField(default=0)


class Tag(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.name


class CommentPost(ModelBase):
    content = models.TextField(max_length=255, null=False)
    post = models.ForeignKey(Post, related_name='comment_post', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.content

class CommentTour(ModelBase):
    content = models.TextField(max_length=255, null=False)
    tour = models.ForeignKey('Tour', related_name='comment_tour', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.content


class ActionPost(ModelBase):
    LIKE, HAHA, SAD, WOW, HEART = range(5)
    ACTIONS = [
        (LIKE, "like"),
        (HAHA, "haha"),
        (SAD, "buồn"),
        (WOW, "wow"),
        (HEART, "trái tim")
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, related_name='action_post', on_delete=models.SET_NULL, null=True)
    type = models.PositiveSmallIntegerField(choices=ACTIONS, default=LIKE)


class Rating(ModelBase):
    tour = models.ForeignKey('Tour', related_name='rating_tour', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rate = models.PositiveSmallIntegerField(default=0)


    def __str__(self):
        return self.rate


class Tour(ModelBase):
    name = models.CharField(null=False, max_length=255)
    tour_type= models.CharField(null=False, max_length=45)
    image = models.ImageField(upload_to='tour/%Y/%m', default=None)
    tour_days = models.IntegerField(default=0)
    tour_nights = models.IntegerField(default=0)
    adults_price = models.IntegerField(null=False)
    children_price = models.IntegerField(null=False)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    introduction = RichTextField(null=True)
    service = RichTextField(null=True)
    note = RichTextField(null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class TourImages(models.Model):
    image = models.ImageField(upload_to='tour-detail/%Y/%m', default=None)
    tour = models.ForeignKey(Tour, related_name='tour_image', on_delete=models.CASCADE)


class TourSchedules(models.Model):
    tour = models.ForeignKey(Tour, related_name="tour_detail_tour", on_delete=models.SET_NULL, null=True)
    departure = models.CharField(max_length=255, null=True)
    destination = models.CharField(max_length=255, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    travel_schedule = RichTextField(null=True)

    def __str__(self):
        return self.departure


class Booking(models.Model):
    price = models.BigIntegerField(null=False)
    adults = models.IntegerField(null=False)
    children = models.IntegerField(null=False)
    active = models.BooleanField(default=True)
    tour = models.ForeignKey(Tour, related_name='booking_tour', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, related_name='booking_user', on_delete=models.SET_NULL, null=True)


class Cancellation(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, primary_key=True)
    reason = models.CharField(max_length=255, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
