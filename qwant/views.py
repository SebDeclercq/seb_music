from __future__ import annotations
from typing import Any, Type
from django.db.models import Manager
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import generic
from django.views.generic.edit import FormView
from qwant.forms import SearchForm
from qwant.music.models import Artist


class ArtistDetailView(generic.DetailView):
    model: Type[Artist] = Artist
    template_name: str = 'qwant/artist_detail.html'


class ArtistsListView(generic.ListView):
    template_name: str = 'qwant/artists_list.html'
    context_object_name: str = _('artists')
    paginate_by: int = 10

    def get_queryset(self) -> Manager[Artist]:
        return Artist.objects.all().order_by('name')


class ArtistSearchView(FormView):
    template_name: str = 'qwant/artist_search.html'
    form_class: Type[SearchForm] = SearchForm

    def form_valid(self, form: SearchForm) -> HttpResponse:
        self.artist: Artist = form.search()
        return super().form_valid(form)

    def get_success_url(self) -> HttpResponse:
        return reverse('qwant:artist_detail', kwargs={'pk': self.artist.pk})


class ArtistReloadView(FormView):
    template_name: str = 'qwant/artist_search.html'
    form_class: Type[SearchForm] = SearchForm

    def form_valid(self, form: SearchForm) -> HttpResponse:
        self.artist: Artist = form.reload()
        return super().form_valid(form)

    def get_success_url(self) -> HttpResponse:
        return reverse('qwant:artist_detail', kwargs={'pk': self.artist.pk})
