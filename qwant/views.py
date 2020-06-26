from __future__ import annotations
from typing import Type
from django.db.models import Manager
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views import generic
from qwant.music.models import Artist


class ArtistDetailView(generic.DetailView):
    model: Type[Artist] = Artist
    template_name: str = 'qwant/artist_detail.html'


class ArtistsListView(generic.ListView):
    template_name: str = 'qwant/artists_list.html'
    context_object_name: str = _('artists')

    def get_queryset(self) -> Manager[Artist]:
        return Artist.objects.all()

