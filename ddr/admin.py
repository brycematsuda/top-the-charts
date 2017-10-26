from django.contrib import admin

# Register your models here.
from .models import Folder
from .models import Song

class FolderAdmin(admin.ModelAdmin):
  list_display = ('name', 'key')

class SongAdmin(admin.ModelAdmin):
  def folder_name(self, obj):
    return obj.folder.name

  folder_name.admin_order_field  = 'folder'  #Allows column order sorting
  folder_name.short_description = 'Folder Name'  #Renames column head

  list_display = ('name', 'artist', 'key', 'folder_name')

admin.site.register(Folder, FolderAdmin)
admin.site.register(Song, SongAdmin)