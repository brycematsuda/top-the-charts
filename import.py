import os
import csv
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "topthecharts.settings")

django.setup()

from ddr.models import Song
from ddr.models import Folder

if __name__ == '__main__':
  folder_list = [
    ('DDR 1st', '1st'),
    ('DDR 2ndMIX', '2nd'),
    ('DDR 3rdMIX', '3rd'),
    ('DDR 4thMIX', '4th'),
    ('DDR 5thMIX', '5th'),
    ('DDRMAX', 'max'),
    ('DDRMAX2', 'max2'),
    ('DDR EXTREME', 'extreme'),
    ('DDR SuperNOVA', 'sn'),
    ('DDR SuperNOVA 2', 'sn2'),
    ('DDR X', 'x'),
    ('DDR X2', 'x2'),
    ('DDR X3 VS 2ndMIX', 'x3'),
    ('DanceDanceRevolution(2013)', 'ddr2013'),
    ('DanceDanceRevolution(2014)', 'ddr2014'),
    ('DDR A', 'a')
  ]

  for (name, key) in folder_list:
    l = Folder()
    l.name = name
    l.key = key
    l.save()

  with open('ddrsonglist.csv', newline='', encoding='utf-8') as csvfile:
   reader = csv.reader(csvfile, delimiter=',', quotechar='"')
   for row in reader:
    l = Song()
    l.name = row[1]
    l.sort_name = row[1]
    l.artist = row[2]
    l.folder = Folder.objects.get(pk=str(row[0]))
    l.single_beginner = row[3] if row[3] != '-' else None
    l.single_basic = row[4] if row[4] != '-' else None
    l.single_difficult = row[5] if row[5] != '-' else None
    l.single_expert = row[6] if row[6] != '-' else None
    l.single_challenge = row[7] if row[7] != '-' else None
    l.double_basic = row[8] if row[8] != '-' else None
    l.double_difficult = row[9] if row[9] != '-' else None
    l.double_expert = row[10] if row[10] != '-' else None
    l.double_challenge = row[11] if row[11] != '-' else None
    l.save()