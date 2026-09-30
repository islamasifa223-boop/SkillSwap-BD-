from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver




class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField(blank=True)

    location = models.CharField(
        max_length=100,
        blank=True
    )

    facebook = models.URLField(blank=True)

    linkedin = models.URLField(blank=True)

    skills = models.CharField(max_length=200, blank=True)

    profile_image = models.ImageField(
        upload_to='profile_images/',
        default='default.png'
    )

    def __str__(self):
        return self.user.username
    
class Skill(models.Model):

    SKILL_TYPE_CHOICES = [
        ('Teach', 'Skill I Can Teach'),
        ('Learn', 'Skill I Want to Learn'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=100)

    category = models.CharField(max_length=100)

    skill_type = models.CharField(
        max_length=10,
        choices=SKILL_TYPE_CHOICES,
        default='Teach'
    )

    description = models.TextField()

    likes = models.ManyToManyField(
        User,
        related_name='liked_skills',
        blank=True
    )

    def __str__(self):
        return self.title

class ExchangeRequest(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_requests'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_requests'
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        default='Pending'
    )

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"
    

    
@receiver(post_save, sender=User)

def create_user_profile(sender, instance, created, **kwargs):

     if created:

        Profile.objects.create(user=instance)

class Like(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE
    )

class Notification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    message = models.CharField(max_length=255)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    
class Follow(models.Model):

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers'
    )

    

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Message(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    message = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"
    
class Session(models.Model):

    exchange_request = models.OneToOneField(
        ExchangeRequest,
        on_delete=models.CASCADE
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='teaching_sessions'
    )

    learner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='learning_sessions'
    )

    session_date = models.DateField()

    session_time = models.TimeField()

    meeting_link = models.URLField(blank=True)

    status = models.CharField(
        max_length=20,
        default='Scheduled'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher} with {self.learner}"
    
class Review(models.Model):

    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='given_reviews'
    )

    reviewed_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_reviews'
    )

    rating = models.IntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} stars by {self.reviewer}"