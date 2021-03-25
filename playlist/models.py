from django.db import models

from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify

from NetFlix.db.models import PublishStateOptions
from NetFlix.db.receivers import publicado_stado_pre_save, slugify_pre_save

from Video.models import Video


class PlayListaQuerySet(models.QuerySet):
	def publicado(self):
		ahora = timezone.now()
		return self.filter(
			stado = PublishStateOptions.PUBLISH,
			tiempo_publicado__lte=ahora
		)

class PlayListaManager(models.Manager):
	def get_queryset(self):
		return PlayListaQuerySet(self.model, using=self._db)

	def publicado(self):
		return self.get_queryset().publicado()


class PlayList(models.Model):

	titulo = models.CharField(max_length=120)
	descripcion = models.TextField(blank=True, null=True)
	slug = models.SlugField(blank=True, null=True)
	activo = models.BooleanField(default=True)
	
	video = models.ForeignKey(Video, related_name='playlist_destacado', blank=True, null=True, on_delete=models.SET_NULL) #un video por lista
	
	videos = models.ManyToManyField(Video, related_name='videos', blank=True, through='PlayListItem')

	timestamp = models.DateTimeField(auto_now_add=True)
	update = models.DateTimeField(auto_now=True)

	stado = models.CharField(max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)

	tiempo_publicado = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

	objects = PlayListaManager()


	@property
	def es_publicado(self):
		return self.activo


class PlayListItem(models.Model):
	playlist = models.ForeignKey(PlayList, on_delete=models.CASCADE)
	video = models.ForeignKey(Video, on_delete=models.CASCADE)
	order = models.IntegerField(default=1)
	timestamp = models.DateTimeField(auto_now_add=True)
	

	class Meta:
		ordering = ['order', '-timestamp']

pre_save.connect(publicado_stado_pre_save, sender=PlayList)
pre_save.connect(slugify_pre_save, sender=PlayList)