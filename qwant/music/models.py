#!/usr/bin/env python3
'''
Module containing the models which collect and use the Qwant Music API data.
Author: SebDeclercq (https://www.github.com/SebDeclercq)
'''
from __future__ import annotations
from typing import Dict, Sequence
from unicodedata import normalize
import re
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from qwant.music.api import API
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
    picture: models.URLField = models.URLField(
        _('Picture'), max_length=1000, blank=True, null=True
    )
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
    def create_from_api(cls, name: str) -> Artist:
        '''Gather data from the Qwant Music API.

        Params:
            name: The artist name to find
        
        Returns:
            The Artist found
        '''
        slug: str = cls.name_to_slug(name)
        data: APIData = API.get(slug)
        return cls.create_from_api_data(**data)

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
        artist, _ = Artist.objects.update_or_create(
            api_id=int(data['id']),
            defaults={
                'name': data['name'],
                'slug': data['slug'],
                'picture': data.get('picture', ''),
            },
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
        sim: Artist = cls.create_from_api_data(**similar_artist)
        artist.similar_artists.add(sim)
        return artist

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('qwant:artist_detail', kwargs={'pk': self.pk})

    @property
    def qwant_url(self) -> str:
        return API.BASE_URL.replace('api', 'www') + self.slug

    @staticmethod
    def name_to_slug(name: str) -> str:
        '''Create the slug based on the artist name.
        1. Clean special characters from the Api.SPECIAL_CHARS
        2. Normalize by removing diacritics
        3. Pass the string to lower
        4. Remove non expected characters
        5. Remove multiple dashes

        Params:
            name: The name to convert to slug

        Returns:
            The formatted slug
        '''
        for special_char in SpecialChar.objects.all():
            name = name.replace(special_char.orig, special_char.dest)
        name: str = (
            normalize('NFKD', name).encode('ascii', 'ignore').decode()
        )
        name = re.sub(r'\s+', '-', name.lower())
        name = re.sub(r'[^-\w]', '', name)
        name = re.sub(r'-+', '-', name)
        return name

    @staticmethod
    def search_or_add(artist_name: str) -> Artist:
        '''Get one Artist data from the API.
        1. Check if the Artist is already in database and return it if it does
        2. Call the API otherwise.
 
        Params:
            artist_name: The name of the Artist to find

        Returns:
            The found Artist
        '''
        try:
            artist_slug: str = Artist.name_to_slug(artist_name)
            return Artist.objects.get(slug=artist_slug)
        except Artist.DoesNotExist:
            return Artist.create_from_api(artist_name)

    def path_to(self, other: Artist, nb_try: int = 1) -> Sequence[Artist]:
        if self._has_direct_relation_with(other):
            return (self, other)
        else:
            self._counter = 0
            return self._search_relation(other, nb_try)

    def _has_direct_relation_with(self, other: Artist) -> bool:
        return any(
            a.api_id == other.api_id for a in self.similar_artists.all()
        )

    def _search_relation(self, other: Artist, nb_try: int) -> Sequence[Artist]:
        for sim in self.similar_artists.all():
            if sim._has_direct_relation_with(other):
                return (self, sim, other)
        return ()


class SpecialChar(models.Model):
    '''Class handling special character to convert in order to create
    the slug from an artist name (example: Møme => Mome).

    Attributes:
        orig: The character to convert (example: 'ø')
        dest: The character to convert to (example: 'o')
    '''

    orig: models.CharField = models.CharField(
        _('Origin character'), max_length=50, blank=False, unique=True
    )
    dest: models.CharField = models.CharField(
        _('Destination character'), max_length=50, blank=False, unique=True
    )

