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
  # Algorithm: Sort all songs, with ones starting with a number going to the bottom of the list  
  songs = sorted(songs, key=lambda k: (k.sort_name[0].lower().isdigit(), k.sort_name.lower()))
  # Filter out Japanese songs and move them to the front of the list
  # (already sorted above provided sort name is in hiragana)    
  alphanum = re.compile(r'^[A-Za-z0-9]+$')
  jp_songs = list(filter(lambda x: not alphanum.match(x.sort_name[0]), songs))
  alphanum_songs = list(filter(lambda x: alphanum.match(x.sort_name[0]), songs))
  songs = jp_songs + alphanum_songs

  return render(request, 'songs/list_by_folder.html', {'folder': folder, 'songs': songs})

def song_list_by_mode_level(request, mode, level):
  beginner_songs = __song_list_mode_level_helper(mode, level, 'beginner')
  basic_songs = __song_list_mode_level_helper(mode, level, 'basic')
  difficult_songs = __song_list_mode_level_helper(mode, level, 'difficult')
  expert_songs = __song_list_mode_level_helper(mode, level, 'expert')
  challenge_songs = __song_list_mode_level_helper(mode, level, 'challenge')

  # Current name sort in DDR is Japanese -> Alphabet -> Number
  # Japanese songs = songs with a sort name that does not start with an alphanumeric character
  # Algorithm: Sort all songs, with ones starting with a number going to the bottom of the list  
  songs = sorted(list(chain(beginner_songs, basic_songs, difficult_songs, expert_songs, challenge_songs)), key=lambda k: (k['sort_name'][0].lower().isdigit(), k['sort_name'].lower()))
  # Filter out Japanese songs and move them to the front of the list
  # (already sorted above provided sort name is in hiragana)
  alphanum = re.compile(r'^[A-Za-z0-9]+$')
  # Can't use set() - set() like in song_list_by_folder because __song_list_mode_level_helper returns a dictionary
  # so create two separate lists with opposite regexes
  jp_songs = list(filter(lambda x: not alphanum.match(x['sort_name'][0]), songs))
  alphanum_songs = list(filter(lambda x: alphanum.match(x['sort_name'][0]), songs))
  songs = jp_songs + alphanum_songs

  return render(request, 'songs/list_by_mode_level.html', {'mode': mode, 'level': level, 'songs': songs})

# Returns list of songs given a mode, difficulty, and level
def __song_list_mode_level_helper(mode, level, difficulty):
  if mode == 'double' and difficulty == 'beginner':
    return Song.objects.none() # double has no beginner charts
  else:    
    mode_diff = mode + '_' + difficulty
    filter_equals = mode_diff + '__exact'
    return (
    Song.objects.filter(**{filter_equals: level}) # kwargs dynamic filter [mode]-[difficulty]=[level] (e.g. single_basic=8)
    .annotate(url=F(mode_diff + '_video')) # add custom field url containg chart video url
    .annotate(difficulty=Value(difficulty, output_field=CharField())) # add custom column 'difficulty' with value being the given difficulty (e.g. difficulty='expert')
    .values('name', 'sort_name', 'artist', 'difficulty', 'url', 'us_locked', 'floor_infection', 'challenge_has_shock_arrows') # get column values, including custom ones created above
    .order_by('sort_name')
    )
