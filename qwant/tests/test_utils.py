#!/usr/bin/env python3
'''
Test module for the utilitarian tools.
Author: SebDeclercq (https://www.github.com/SebDeclercq)
'''
from typing import Sequence, Tuple
import pytest
from qwant.music.utils import ArtistManager


names_and_id: Sequence[Tuple[str, int]] = (
    ('Goldroom', 260920179),
    ('Satin Jackets', 441748199),
)


class TestArtistManager:
    @pytest.mark.real_api_call
    @pytest.mark.django_db
    @pytest.mark.parametrize('name,api_id', names_and_id)
    def test_get_one(self, name: str, api_id: int) -> None:
        assert ArtistManager.search_or_add(name).api_id == api_id
