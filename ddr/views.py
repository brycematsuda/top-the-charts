from django.shortcuts import render
from django.http import Http404
from django.db.models import Value, CharField, F
from itertools import chain
import re

from .models import Song
from .models import Folder

def index(request):
  return render(request, 'index.html')

def songs_index(request):
  folders = Folder.objects.all()
  return render(request, 'songs/index.html', {'folders': folders})

def song_list_by_folder(request, folder_key):
  try:
    folder = Folder.objects.get(key=folder_key)
    songs = Song.objects.filter(folder=folder).order_by('sort_name')
  except Folder.DoesNotExist:
    raise Http404("Folder does not exist")
  
  # Songs that start with a number go to the bottom of the list
  # (need to find a way to move songs that start with a Japanese character to the top)
  songs = sorted(songs, key=lambda k: (k.sort_name[0].lower().isdigit(), k.sort_name.lower())) 
  return render(request, 'songs/list_by_folder.html', {'folder': folder, 'songs': songs})

def song_list_by_mode_level(request, mode, level):
  # Need to find a better way to do this... :\
  if mode == 'single':
     beginner_songs = Song.objects.filter(single_beginner=level).annotate(url=F('single_beginner_video')).annotate(difficulty=Value('beginner', output_field=CharField())).values('name', 'sort_name', 'artist', 'difficulty', 'url').order_by('sort_name')
     basic_songs = Song.objects.filter(single_basic=level).annotate(url=F('single_basic_video')).annotate(difficulty=Value('basic', output_field=CharField())).values('name', 'sort_name', 'artist', 'difficulty', 'url').order_by('sort_name')
     difficult_songs = Song.objects.filter(single_difficult=level).annotate(url=F('single_difficult_video')).annotate(difficulty=Value('difficult', output_field=CharField())).values('name', 'sort_name', 'artist', 'difficulty', 'url').order_by('sort_name')
     expert_songs = Song.objects.filter(single_expert=level).annotate(url=F('single_expert_video')).annotate(difficulty=Value('expert', output_field=CharField())).values('name', 'sort_name', 'artist', 'difficulty', 'url').order_by('sort_name')
     challenge_songs = Song.objects.filter(single_challenge=level).annotate(url=F('single_challenge_video')).annotate(difficulty=Value('challenge', output_field=CharField())).values('name', 'sort_name', 'artist', 'difficulty', 'url').order_by('sort_name')
  elif mode == 'double':
    beginner_songs = Song.objects.none() # double has no beginner difficulty
    basic_songs = Song.objects.filter(double_basic=level).annotate(url=F('double_basic_video')).annotate(difficulty=Value('basic', output_field=CharField())).values('name', 'sort_name', 'artist', 'difficulty', 'url').order_by('sort_name')
    difficult_songs = Song.objects.filter(double_difficult=level).annotate(url=F('double_difficult_video')).annotate(difficulty=Value('difficult', output_field=CharField())).values('name', 'sort_name', 'artist', 'difficulty', 'url').order_by('sort_name')
    expert_songs = Song.objects.filter(double_expert=level).annotate(url=F('double_expert_video')).annotate(difficulty=Value('expert', output_field=CharField())).values('name', 'sort_name', 'artist', 'difficulty').order_by('sort_name')
    challenge_songs = Song.objects.filter(double_challenge=level).annotate(url=F('double_challenge_video')).annotate(difficulty=Value('challenge', output_field=CharField())).values('name', 'sort_name', 'artist', 'difficulty', 'url').order_by('sort_name')
  
  # Songs that start with a number go to the bottom of the list
  # (need to find a way to move songs that start with a Japanese character to the top)  
  songs = sorted(list(chain(beginner_songs, basic_songs, difficult_songs, expert_songs, challenge_songs)), key=lambda k: (k['sort_name'][0].lower().isdigit(), k['sort_name'].lower()))
  
  return render(request, 'songs/list_by_mode_level.html', {'mode': mode, 'level': level, 'songs': songs})