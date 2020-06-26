#!/usr/bin/env python3
'''
Simple script to populate the database. Create a small sample of artists.
Author: SebDeclercq (https://www.github.com/SebDeclercq)
'''
from typing import Any, List, Sequence
from django.core.management.base import (
    BaseCommand,
    CommandError,
    CommandParser,
)
from qwant.music.models import Artist


class ArtistCLIManager:
    '''Add a new artist from the command line.'''

    @staticmethod
    def add(artist_name: str) -> Artist:
        '''Main method of ArtistCLIManager.
    
        Returns:
            The inserted Artist
        '''
        return Artist.create_from_api(artist_name)


class Command(BaseCommand):
    '''Django Custom Command Class to add an artist in the database.'''

    help: str = 'Add a new artist'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('-n', '--name', type=str, help='The Artist name')

    def handle(self, *args: Any, **options: Any) -> None:
        try:
            artist_name = options['name']
            ArtistCLIManager.add(artist_name)
        except KeyError:
            raise CommandError('Provide an artist name w/ -n or --name')
