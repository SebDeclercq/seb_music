#!/usr/bin/env python3
'''
Module containing the models which collect and use the Qwant Music API data.
Author: SebDeclercq (https://www.github.com/SebDeclercq)
'''
from __future__ import annotations
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from qwant.music.types import APIData


class Artist(models.Model):
    '''Class representing the Qwant Music API result in database.
    
    Attributes:
        name: The artist name.
        slug: The artist slug.
        api_id: The ID of the artist in the Qwant Music API.

    '''

    name: models.CharField = models.CharField(_('Name'), max_length=255)
    slug: models.SlugField = models.SlugField(_('Slug'))
    api_id: models.IntegerField = models.IntegerField(_('Qwant API id'))

    class Meta:
        verbose_name = _('artist')
        verbose_name_plural = _('artists')

    @classmethod
    def create_from_api_data(cls, **data: APIData) -> Artist:
        artist: cls = cls(
            name=data['name'], slug=data['slug'], api_id=data['id']
        )
        return artist

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('qwant:artist_detail', kwargs={'pk': self.pk})
