from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, Book, BookSpecifications


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Book)
def create_book_specifications(sender, instance, created, **kwargs):
    if created:
        BookSpecifications.objects.create(book=instance, book_code=f"BOOK-{instance.id}")