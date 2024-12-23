import re
import uuid
import secrets

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from validators.domain import domain

from django_resized import ResizedImageField

from dynamic_filenames import FilePattern

import dns.resolver

import requests

# Create your models here.


class User(AbstractUser):
    """
    User model.
    """

    def generate_secret_key():
        return secrets.token_urlsafe(192)

    def username_validator(username):
        if not re.match(r"^([0-9]|[a-z]|_|\.)+$", username) and len(username) >= 4:
            raise ValidationError("Invalid username.")

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, null=False
    )
    username = models.CharField(
        "username",
        max_length=32,
        unique=True,
        help_text="Required. 32 characters or fewer. Lowercase letters, digits and /./_ only.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )

    secret_key = models.CharField(max_length=256, default=generate_secret_key)

    nickname = models.CharField(max_length=50, null=True, blank=True)

    biography = models.CharField(max_length=500, null=True, blank=True)

    avatar_image = ResizedImageField(
        size=[512, 512],
        crop=["middle", "center"],
        upload_to=FilePattern(
            filename_pattern="user/avatar/{uuid:base32}{ext}"
        ),
        blank=True,
        null=True,
    )

    liked_images = models.ManyToManyField(
        "images.Image", blank=True, related_name="liked_by"
    )
    saved_images = models.ManyToManyField(
        "images.Image", blank=True, related_name="saved_by"
    )

    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
    followed_characters = models.ManyToManyField(
        "characters.Character", related_name="followers"
    )
    followed_categories = models.ManyToManyField(
        "categories.Category", related_name="followers"
    )
    followed_artists = models.ManyToManyField(
        "artists.Artist", related_name="followers"
    )
    followed_lists = models.ManyToManyField("lists.List", related_name="followers")


class DiscordUser(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True, unique=True)
    email = models.EmailField(unique=True)
    user = models.OneToOneField(
        User, unique=True, related_name="discord", on_delete=models.CASCADE
    )

    access_token = models.CharField(max_length=256)
    refresh_token = models.CharField(max_length=256)


class GoogleUser(models.Model):
    id = models.CharField(
        primary_key=True, null=False, blank=False, unique=True, max_length=256
    )
    email = models.EmailField(null=False, blank=False, unique=True)
    user = models.OneToOneField(
        User, unique=True, related_name="google", on_delete=models.CASCADE
    )


class GitHubUser(models.Model):
    class Meta:
        verbose_name = "GitHub User"
        verbose_name_plural = "GitHub Users"

    id = models.PositiveBigIntegerField(
        primary_key=True, unique=True, blank=False, null=False
    )
    email = models.EmailField(null=False, blank=False)
    user = models.OneToOneField(User, related_name="github", on_delete=models.CASCADE)
