from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^ddr/songs/?$', views.songs_index, name='songs index'),
  url(r'^ddr/songs/folder/(?P<folder_key>[a-z0-9]*[a-z]+([a-z0-9]+)*([a-z0-9])*)/?$', views.song_list_by_folder, name='song list by folder'),
  url(r'^ddr/songs/(?P<mode>(single|double))/(?P<level>(1[0-9]|[1-9])$)/?$', views.song_list_by_mode_level, name='song list by mode level'),  
]