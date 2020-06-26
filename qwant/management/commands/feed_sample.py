#!/usr/bin/env python3
'''
Simple script to populate the database. Create a small sample of artists.
Author: SebDeclercq (https://www.github.com/SebDeclercq)
'''
from typing import Any, List, Sequence
from django.core.management.base import BaseCommand
from qwant.music.models import Artist


class DbSampler:
    '''Gather some artists from the unofficial Qwant Music API
    to add sample data in the database'''

    ARTIST_NAMES: Sequence[str] = (
        'Satin Jackets',
        'Flight Facilities',
        'Bonobo',
        'Tycho',
        'Daft Punk',
        'Thylacine',
        'RÜFÜS DU SOL',
    )

    @staticmethod
    def feed_db() -> List[Artist]:
        '''Main method of DbSampler.
        
        Returns:
            The list of the inserted Artists
        '''
        artists: List[Artist] = []
        for artist_name in DbSampler.ARTIST_NAMES:
            artist: Artist = Artist.create_from_api(artist_name)
            artists.append(artist)
        return artists


class Command(BaseCommand):
    '''Django Custom Command Class to add a sample artists in the database.'''

    help: str = 'Create a small sample of artists'

    def handle(self, *args: Any, **options: Any) -> None:
        DbSampler.feed_db()
