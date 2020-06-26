#!/usr/bin/env python3
'''
Utilitarian tools for interacting w/ the unofficial Qwant Music API
Author: SebDeclercq (https://www.github.com/SebDeclercq)
'''
from qwant.music.models import Artist


class ArtistManager:
    '''Manage actions with the Artist model.'''

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
