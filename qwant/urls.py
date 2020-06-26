from typing import List
from django.urls import path
from django.urls.resolvers import URLPattern
from django.utils.translation import gettext as _
from qwant import views


app_name: str = _('qwant')


urlpatterns: List[URLPattern] = [
    path(
        _('music/artist/id/<int:pk>'),
        views.ArtistDetailView.as_view(),
        name=_('artist_detail'),
    ),
    path(
        _('music/artist/'),
        views.ArtistsListView.as_view(),
        name=_('artists_list'),
    ),
    path(
        _('music/artist/search/'),
        views.ArtistSearchView.as_view(),
        name=_('artist_search'),
    ),
]
