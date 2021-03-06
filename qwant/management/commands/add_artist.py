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


class Command(BaseCommand):
    '''Django Custom Command Class to add an artist in the database.'''

    help: str = 'Add a new artist'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('-n', '--name', type=str, help='The Artist name')

    def handle(self, *args: Any, **options: Any) -> None:
        artist_name = options['name']
        Artist.search_or_add(artist_name)
