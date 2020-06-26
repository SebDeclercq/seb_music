#!/usr/bin/env python3
'''
Utilitarian tools for interacting w/ the unofficial Qwant Music API
Author: SebDeclercq (https://www.github.com/SebDeclercq)
'''
from qwant.music.models import Artist


class ArtistManager:
    '''Add a new artist.'''

    @staticmethod
    def add(artist_name: str) -> Artist:
        '''Main method of ArtistCLIManager.
    
        Returns:
            The inserted Artist
        '''
        return Artist.create_from_api(artist_name)
