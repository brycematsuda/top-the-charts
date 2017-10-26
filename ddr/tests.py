from django.test import TestCase
from django.test import Client
from django.core.exceptions import ValidationError
from ddr.models import Folder
from ddr.models import Song
from selenium import webdriver

class SeleniumTest(TestCase):
  def setUp(self):
    firefox_profile = webdriver.FirefoxProfile()
    self.browser = webdriver.Firefox(firefox_profile)

  def tearDown(self):
    self.browser.quit()

  def test_charts(self):
    self.browser.get('http://localhost:8000/ddr/songs/folder/a')
    self.assertIn('Top The Charts - DDR - Songs - DDR A', self.browser.title)

class ResponseTest(TestCase):
  def setUp(self):
    self.client = Client()
    folder = Folder.objects.create(name='DDR A', key='a')
    Song.objects.create(name='Test Name', artist='Test Artist', folder=folder, single_expert='18')

  def test_responses(self):
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)
    response = self.client.get('/ddr/songs/')
    self.assertEqual(response.status_code, 200)
    response = self.client.get('/ddr/songs/single/18')
    self.assertEqual(response.status_code, 200)
    response = self.client.get('/ddr/songs/single/02')
    self.assertEqual(response.status_code, 404)
    response = self.client.get('/ddr/songs/single/21')
    self.assertEqual(response.status_code, 404)
    response = self.client.get('/ddr/songs/single/100')
    self.assertEqual(response.status_code, 404)
    response = self.client.get('/ddr/songs/folder/a')
    self.assertEqual(response.status_code, 200)
    response = self.client.get('/ddr/songs/folder/aa')
    self.assertEqual(response.status_code, 404)

class FolderModelsTest(TestCase):
  def test_folder_unit(self):
    folder = Folder.objects.create(name='test folder', key='key')
    self.assertEqual(folder.name, 'test folder')
    self.assertEqual(folder.key, 'key')
  
  def test_folder_key_validations(self):
    with self.assertRaises(ValidationError):
      bad_keys = ['TESTNAME', 'TestName', '12', 'test name', 'test_name', 'test-name', 'testname?', '♥Love²シュガ→♥']
      for key in bad_keys:
        folder = Folder(name='test name', key=key)
        folder.full_clean()

class SongModelsTest(TestCase):
  def test_song_unit(self):
    song = Song.objects.create(name='test song', artist='test artist', key='key')
    self.assertEqual(song.name, 'test song')
    self.assertEqual(song.artist, 'test artist')
    self.assertEqual(song.key, 'key')

  def test_song_key_validations(self):
    with self.assertRaises(ValidationError):
      bad_keys = ['TESTNAME', 'TestName', '12', 'test name', 'test_name', 'test-name', 'testname?', '♥Love²シュガ→♥']
      for key in bad_keys:
        song = Song(name='test name', artist='test artist', key=key)
        song.full_clean()

  def test_default_sort_name_if_blank(self):
    song = Song.objects.create(name='test name', artist='test artist')
    self.assertEqual(song.sort_name, 'test name')