#!/usr/bin/env python3
'''
Module containing the models which collect and use the Qwant Music API data.
Author: SebDeclercq (https://www.github.com/SebDeclercq)
'''
from __future__ import annotations
from typing import Dict
from unicodedata import normalize
import re
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
        similar_artists (optional): Similar artists listed by the API.
    '''

    name: models.CharField = models.CharField(
        _('Name'), max_length=255, blank=False
    )
    slug: models.SlugField = models.SlugField(_('Slug'), unique=True)
    api_id: models.IntegerField = models.IntegerField(
        _('Qwant API id'), unique=True
    )
    similar_artists: models.ManyToManyField = models.ManyToManyField(
        'self', verbose_name=_('Similar Artists')
    )

    class Meta:
        verbose_name: str = _('artist')
        verbose_name_plural: str = _('artists')

    @classmethod
    def create_from_api_data(cls, **data: APIData) -> Artist:
        '''Parse the data provided by the Qwant Music API to
        create a new Artist.

        Params:
            data: APIData

        Returns:
            Artist: the created instance
        '''
        artist: Artist
        artist, _ = Artist.objects.get_or_create(
            name=data['name'], slug=data['slug'], api_id=data['id']
        )
        if similar_artists := data.get('similar_artists'):
            for similar_artist in similar_artists:
                cls._add_similar_artist(artist, similar_artist)
        return artist

    @classmethod
    def _add_similar_artist(
        cls, artist: Artist, similar_artist: Dict[str, str]
    ) -> Artist:
        '''Add a similar Artist to an Artist.

        Params:
            artist: The Artist for whom to add a similar Artist
            similar_artist: The API Data for the similar Artist

        Returns:
            Artist: The updated Artist
        '''
        sim: Artist
        sim, _ = Artist.objects.get_or_create(
            name=similar_artist['name'],
            slug=similar_artist['slug'],
            api_id=similar_artist['id'],
        )
        artist.similar_artists.add(sim)
        return artist

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('qwant:artist_detail', kwargs={'pk': self.pk})

    @staticmethod
    def name_to_slug(name: str) -> str:
        '''Create the slug based on the artist name.
        1. Normalize by removing diacritics
        2. Pass the string to lower
        3. Remove non expected characters
        4. Remove multiple dashes

        Params:
            name: The name to convert to slug

        Returns:
            The formatted slug
        '''
        name: str = (
            normalize('NFKD', name).encode('ascii', 'ignore').decode()
        )
        name = re.sub(r'\s+', '-', name.lower())
        name = re.sub(r'[^-\w]', '', name)
        name = re.sub(r'-+', '-', name)
        return name
