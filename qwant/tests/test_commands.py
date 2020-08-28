#!/usr/bin/env python3
'''
Test module for the custom commands.
Author: SebDeclercq (https://www.github.com/SebDeclercq)
'''
from django.core.management import call_command, CommandError
from _pytest.monkeypatch import MonkeyPatch
import pytest
from qwant.management.commands.feed_sample import DbSampler
from qwant.music.models import Artist


class TestAddArtistCommand:
    @pytest.mark.real_api_call
    @pytest.mark.django_db
    def test_add_artist(self) -> None:
        nb_artist: int = Artist.objects.count()
        call_command('add_artist', *[], **{'name': 'Ofenbach'})
        assert Artist.objects.count() > nb_artist

    @pytest.mark.django_db
    def test_add_artist_no_name_fail(self) -> None:
        with pytest.raises(TypeError):
            call_command('add_artist', *[], **{'unknown': ''})
        with pytest.raises((CommandError, TypeError)):
            call_command('add_artist', *[], **{})


class TestDbSamplerCommand:
    @pytest.mark.real_api_call
    @pytest.mark.django_db
    def test_insert_one(self, monkeypatch: MonkeyPatch) -> None:
        DbSampler.ARTIST_NAMES = 'Feder'
        nb_artist: int = Artist.objects.count()
        call_command('feed_sample', *[], **{})
        assert Artist.objects.count() > nb_artist
