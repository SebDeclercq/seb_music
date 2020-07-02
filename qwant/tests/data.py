#!/usr/bin/env python3
'''
Data samples used for parametrized tests
Author: SebDeclercq (https://www.github.com/SebDeclercq)
'''
from typing import List, Sequence, Tuple
from qwant.music.types import APIData

API_DATA: List[APIData] = [
    {
        'name': 'Artist-1',
        'slug': 'artist-1',
        'id': 123456,
        'similar_artists': [
            {'name': 'Similar-1', 'slug': 'similar-1', 'id': 789123},
            {'name': 'Similar-2', 'slug': 'similar-2', 'id': 147258},
        ],
        'picture': 'http://www.example.org/pic1',
    },
    {
        'name': 'Artist-2',
        'slug': 'artist-2',
        'id': 456789,
        'similar_artists': [],
    },
    {
        'name': 'Artist-3',
        'slug': 'artist-3',
        'id': 654321,
        'similar_artists': [
            {'name': 'Artist-4', 'slug': 'artist-4', 'id': 987654},
            {'name': 'Artist-5', 'slug': 'artist-5', 'id': 876543},
        ],
    },
    {
        'name': 'Artist-4',
        'slug': 'artist-4',
        'id': 987654,
        'similar_artists': [
            {'name': 'Artist-3', 'slug': 'artist-3', 'id': 654321},
        ],
    },
    {
        'name': 'Artist-5',
        'slug': 'artist-5',
        'id': 876543,
        'similar_artists': [
            {'name': 'Artist-3', 'slug': 'artist-3', 'id': 654321},
        ],
    },
    {
        'name': 'Artist-6',
        'slug': 'artist-6',
        'id': 345678,
        'similar_artists': [
            {'name': 'Artist-4', 'slug': 'artist-4', 'id': 987654},
        ],
    },
]


NAMES_AND_SLUGS: Sequence[Tuple[str, str]] = (
    ('hello', 'hello'),
    ('Hello', 'hello'),
    ('Hello World', 'hello-world'),
    ('Tiësto', 'tiesto'),
    ('Satin- -Jackets', 'satin-jackets'),
    ('==hel++lo==', 'hello'),
    ('Blank & Jones', 'blank-jones'),
    ('Møme', 'mome'),
)


NAMES_AND_DATA: Sequence[Tuple[str, APIData]] = (
    (
        'Goldroom',
        {
            'slug': 'goldroom',
            'id': 260920179,
            'similar_artist_name': 'Satin Jackets',
        },
    ),
    (
        'Satin Jackets',
        {
            'slug': 'satin-jackets',
            'id': 441748199,
            'similar_artist_name': 'Goldroom',
        },
    ),
)

NAMES_AND_ID: Sequence[Tuple[str, int]] = (
    ('Goldroom', 260920179),
    ('Satin Jackets', 441748199),
)
