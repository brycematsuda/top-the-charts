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
  
  songs = list(songs)
  # Current name sort in DDR is Japanese -> Alphabet -> Number
  # Japanese songs = songs with a sort name that does not start with an alphanumeric character
  # Algorithm: Separate Japanese songs into their own list
  alphanum = re.compile(r'^[A-Za-z0-9]+$')
  jp_songs = list(filter(lambda x: not alphanum.match(x.sort_name[0]), songs))
  # Sort all other songs, putting number songs last
  # (Japanese songs will already be sorted correctly provided sort name is only in hiragana  
  alphanum_songs = list(set(songs) - set(jp_songs))
  alphanum_songs = sorted(alphanum_songs, key=lambda k: (k.sort_name[0].lower().isdigit(), k.sort_name.lower()))  
  # Put Japanese songs at the front of the main song list.
  songs = jp_songs + alphanum_songs

  return render(request, 'songs/list_by_folder.html', {'folder': folder, 'songs': songs})

def song_list_by_mode_level(request, mode, level):
  # Need to find a better way to do this... :\
  if mode == 'single':
     beginner_songs = Song.objects.filter(single_beginner=level).annotate(url=F('single_beginner_video')).annotate(difficulty=Value('beginner', output_field=CharField())).values('name', 'sort_name', 'artist', 'difficulty', 'url', 'us_locked', 'floor_infection').order_by('sort_name')
     basic_songs = Song.objects.filter(single_basic=level).annotate(url=F('single_basic_video')).annotate(difficulty=Value('basic', output_field=CharField())).values('name', 'sort_name', 'artist', 'difficulty', 'url', 'us_locked', 'floor_infection').order_by('sort_name')
     difficult_songs = Song.objects.filter(single_difficult=level).annotate(url=F('single_difficult_video')).annotate(difficulty=Value('difficult', output_field=CharField())).values('name', 'sort_name', 'artist', 'difficulty', 'url', 'us_locked', 'floor_infection').order_by('sort_name')
     expert_songs = Song.objects.filter(single_expert=level).annotate(url=F('single_expert_video')).annotate(difficulty=Value('expert', output_field=CharField())).values('name', 'sort_name', 'artist', 'difficulty', 'url', 'us_locked', 'floor_infection').order_by('sort_name')
     challenge_songs = Song.objects.filter(single_challenge=level).annotate(url=F('single_challenge_video')).annotate(difficulty=Value('challenge', output_field=CharField())).values('name', 'sort_name', 'artist', 'difficulty', 'url', 'us_locked', 'floor_infection').order_by('sort_name')
  elif mode == 'double':
    beginner_songs = Song.objects.none() # double has no beginner difficulty
    basic_songs = Song.objects.filter(double_basic=level).annotate(url=F('double_basic_video')).annotate(difficulty=Value('basic', output_field=CharField())).values('name', 'sort_name', 'artist', 'difficulty', 'url', 'us_locked', 'floor_infection').order_by('sort_name')
    difficult_songs = Song.objects.filter(double_difficult=level).annotate(url=F('double_difficult_video')).annotate(difficulty=Value('difficult', output_field=CharField())).values('name', 'sort_name', 'artist', 'difficulty', 'url', 'us_locked', 'floor_infection').order_by('sort_name')
    expert_songs = Song.objects.filter(double_expert=level).annotate(url=F('double_expert_video')).annotate(difficulty=Value('expert', output_field=CharField())).values('name', 'sort_name', 'artist', 'difficulty').order_by('sort_name')
    challenge_songs = Song.objects.filter(double_challenge=level).annotate(url=F('double_challenge_video')).annotate(difficulty=Value('challenge', output_field=CharField())).values('name', 'sort_name', 'artist', 'difficulty', 'url', 'us_locked', 'floor_infection').order_by('sort_name')
  
  # Current name sort in DDR is Japanese -> Alphabet -> Number
  # Japanese songs = songs with a sort name that does not start with an alphanumeric character
  # Algorithm: Sort all songs, with ones start with a number go to the bottom of the list
  songs = sorted(list(chain(beginner_songs, basic_songs, difficult_songs, expert_songs, challenge_songs)), key=lambda k: (k['sort_name'][0].lower().isdigit(), k['sort_name'].lower()))
  # Filter out Japanese songs and move them to the front of the list
  # (already sorted above provided sort name is in hiragana)
  alphanum = re.compile(r'^[A-Za-z0-9]+$')
  jp_songs = list(filter(lambda x: not alphanum.match(x['sort_name'][0]), songs))
  songs = list(filter(lambda x: alphanum.match(x['sort_name'][0]), songs))
  songs = jp_songs + songs

  return render(request, 'songs/list_by_mode_level.html', {'mode': mode, 'level': level, 'songs': songs})