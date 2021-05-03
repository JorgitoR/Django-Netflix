from django.shortcuts import render

from django.views.generics import ListView, DetailView

from .models import categoria

from django.http import Htpp404

from django.db.models import Count

from playlist.models import PlayList
from playlist.mixins import PlayListMixin