#!/usr/bin/env python3
'''
Test module for the views of the Qwant Django App.
Author: SebDeclercq (https://www.github.com/SebDeclercq)
'''
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
import pytest
from qwant.music.models import Artist


@pytest.fixture
def artist() -> Artist:
    return Artist.objects.create(
        name='my artist', slug='my-artist', api_id=123
    )


class TestArtistDetailView:
    @pytest.mark.django_db
    def test_get_one(self, artist: Artist) -> None:
        client: Client = Client()
        resp: HttpResponse = client.get(
            reverse('qwant:artist_detail', args=[artist.pk]),
        )
        assert resp.status_code == 200
        assert 'qwant/artist_detail.html' in resp.template_name
        assert artist.name in resp.content.decode('utf-8')


class TestArtistsList:
    @pytest.mark.django_db
    def test_get_list(self, artist: Artist) -> None:
        client: Client = Client()
        resp: HttpResponse = client.get(reverse('qwant:artists_list'))
        assert resp.status_code == 200
        assert 'qwant/artist_list.html' in resp.template_name
        assert artist in resp.context['artists']


class TestArtistSearch:
    @pytest.mark.real_api_call
    @pytest.mark.django_db
    def test_get_artist(self) -> None:
        client: Client = Client()
        resp: HttpResponse = client.post(
            reverse('qwant:artist_search'),
            {'artist_name': 'Moby'},
            follow=True,
        )
        assert resp.status_code == 200
        assert 'qwant/artist_detail.html' in resp.template_name

    @pytest.mark.real_api_call
    @pytest.mark.django_db
    def test_get_artist_no_result(self) -> None:
        client: Client = Client()
        resp: HttpResponse = client.post(
            reverse('qwant:artist_search'),
            {'artist_name': 'czfzpoeéçfnecze'},
            follow=True,
        )
        assert resp.status_code == 404


class TestArtistReload:
    @pytest.mark.real_api_call
    @pytest.mark.django_db
    def test_reload_artist(self) -> None:
        client: Client = Client()
        resp: HttpResponse = client.post(
            reverse('qwant:artist_reload'),
            {'artist_name': 'Moby'},
            follow=True,
        )
        assert resp.status_code == 200
        assert 'qwant/artist_detail.html' in resp.template_name
