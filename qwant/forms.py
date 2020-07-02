#!/usr/bin/env python3
'''
Module containing the forms for the UI.
Author: SebDeclercq (https://www.github.com/SebDeclercq)
'''
from django import forms
from django.utils.translation import gettext as _
from qwant.music.models import Artist


class SearchForm(forms.Form):
    artist_name: forms.CharField = forms.CharField(
        label=_('Artist name'), max_length=200, required=True
    )

    def search(self) -> Artist:
        '''Search for an Artist in the database or else get it from the API,
        insert it and return it.
        
        Returns:
            The asked for Artist.
        '''
        return Artist.search_or_add(self.cleaned_data['artist_name'])

    def reload(self) -> Artist:
        return Artist.create_from_api(self.cleaned_data['artist_name'])
