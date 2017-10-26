from django.db import models
from django.core.validators import RegexValidator

LEVEL_CHOICES = (
  ('1', '1'),
  ('2', '2'),
  ('3', '3'),
  ('4', '4'),
  ('5', '5'),
  ('6', '6'),
  ('7', '7'),
  ('8', '8'),
  ('9', '9'),
  ('10', '10'),
  ('11', '11'),
  ('12', '12'),
  ('13', '13'),
  ('14', '14'),
  ('15', '15'),
  ('16', '16'),
  ('17', '17'),
  ('18', '18'),
  ('19', '19')
)

class EmptyStringToNoneField(models.CharField):
  def get_prep_value(self, value):
    if value != None and value.strip() == '':
      return None  
    return value
    
# Create your models here.
class Folder(models.Model):
  key_validator = RegexValidator(r'[a-z0-9]*[a-z]+([a-z0-9]+)*([a-z0-9])*', 'Keys can only have lowercase letters and numbers. Keys must contain at least one letter.')

  name = models.CharField(max_length=100)
  key = EmptyStringToNoneField(max_length=50, validators=[key_validator], blank=True, unique=True, null=True)

  def __str__(self):
    return self.name

class Song(models.Model):
  key_validator = RegexValidator(r'[a-z0-9]*[a-z]+([a-z0-9]+)*([a-z0-9])*', 'Keys can only have lowercase letters and numbers. Keys must contain at least one letter.')

  name = EmptyStringToNoneField(max_length=100)
  sort_name = models.CharField(max_length=100)
  artist = EmptyStringToNoneField(max_length=100)
  key = EmptyStringToNoneField(max_length=50, validators=[key_validator], blank=True, unique=True, null=True)
  folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True)    
  us_locked = models.BooleanField(default=False)
  floor_infection = models.BooleanField(default=False)
  removed = models.BooleanField(default=False)     
  challenge_has_shock_arrows = models.BooleanField(default=False)    
  single_beginner = EmptyStringToNoneField(max_length=2, choices=LEVEL_CHOICES, blank=True, null=True)
  single_beginner_video = EmptyStringToNoneField(max_length=100, blank=True, null=True)
  single_basic = EmptyStringToNoneField(max_length=2, choices=LEVEL_CHOICES, blank=True, null=True)
  single_basic_video = EmptyStringToNoneField(max_length=100, blank=True, null=True)    
  single_difficult = EmptyStringToNoneField(max_length=2, choices=LEVEL_CHOICES, blank=True, null=True)
  single_difficult_video = EmptyStringToNoneField(max_length=100, blank=True, null=True)    
  single_expert = EmptyStringToNoneField(max_length=2, choices=LEVEL_CHOICES, blank=True, null=True)
  single_expert_video = EmptyStringToNoneField(max_length=100, blank=True, null=True)    
  single_challenge = EmptyStringToNoneField(max_length=2, choices=LEVEL_CHOICES, blank=True, null=True)
  single_challenge_video = EmptyStringToNoneField(max_length=100, blank=True, null=True)    
  double_basic = EmptyStringToNoneField(max_length=2, choices=LEVEL_CHOICES, blank=True, null=True)
  double_basic_video = EmptyStringToNoneField(max_length=100, blank=True, null=True)    
  double_difficult = EmptyStringToNoneField(max_length=2, choices=LEVEL_CHOICES, blank=True, null=True)
  double_difficult_video = EmptyStringToNoneField(max_length=100, blank=True, null=True)    
  double_expert = EmptyStringToNoneField(max_length=2, choices=LEVEL_CHOICES, blank=True, null=True)
  double_expert_video = EmptyStringToNoneField(max_length=100, blank=True, null=True)    
  double_challenge = EmptyStringToNoneField(max_length=2, choices=LEVEL_CHOICES, blank=True, null=True)
  double_challenge_video = EmptyStringToNoneField(max_length=100, blank=True, null=True)    
  #last_updated = models.DateTimeField(auto_now_add=True) will add back in once all song videos have been added

  def save(self, *args, **kwargs):
    # default sort name to regular name if blank
    if not self.sort_name or self.sort_name.strip() == '':
      self.sort_name = self.name
    super().save(*args, **kwargs)

  def __str__(self):
    return self.name