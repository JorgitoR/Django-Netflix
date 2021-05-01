from django.contrib.contenttypes.fields import GenericRelation


from django.db import models
from django.db.models import Avg, Max, Min, Q

from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify

from NetFlix.db.models import PublishStateOptions
from NetFlix.db.receivers import publicado_stado_pre_save, slugify_pre_save


from Video.models import Video
from categoria.models import categoria
from tags.models import  TaggedItem
from clasificacion.models import Clasificacion

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

	def playlist_destacados(self):
		return self.get_queryset().filter(type=PlayList.PlaylistTypeChoices.PLAYLIST)

class PlayList(models.Model):
	class PlaylistTypeChoices(models.TextChoices):
		MOVIE= "MOV", "Movie",
		SHOW = "TVS", "TV Show",
		SEASON = "SEA", "Season",
		PLAYLIST = "PLY", "PlayList"

	padre = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL)
	order = models.IntegerField(default=1)	

	titulo = models.CharField(max_length=120)

	type = models.CharField(max_length=3, choices=PlaylistTypeChoices.choices, default=PlaylistTypeChoices.PLAYLIST)

	categoria = models.ForeignKey(categoria, related_name='playlist', blank=True, null=True, on_delete=models.SET_NULL)

	descripcion = models.TextField(blank=True, null=True)
	slug = models.SlugField(blank=True, null=True)
	activo = models.BooleanField(default=True)
	
	video = models.ForeignKey(Video, related_name='playlist_destacado', blank=True, null=True, on_delete=models.SET_NULL) #un video por lista
	
	videos = models.ManyToManyField(Video, related_name='videos', blank=True, through='PlayListItem')

	timestamp = models.DateTimeField(auto_now_add=True)
	update = models.DateTimeField(auto_now=True)

	stado = models.CharField(max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)

	tiempo_publicado = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

	tags = GenericRelation(TaggedItem, related_query_name='playlist')
	clasificacion = GenericRelation(Clasificacion, related_query_name='playlist')

	objects = PlayListaManager()

	#class Meta:
		#unique_together =(('titulo', 'slug'))

	def __str__(self):
		return self.titulo

	@property
	def es_publicado(self):
		return self.activo

	def get_clasificacion_avg(self):
		return PlayList.objects.filter(id=self.id).aggregate(Avg("clasificacion__valor"))

	def get_clasificacion_max_min(self):
		return PlayList.objects.filter(id=self.id).aggregate(max=Max("clasificacion__valor"), min=Min("clasificacion__valor"))


	def get_corto_display(self):
		return ""


class PlaylistaItemQueryset(models.QuerySet):
	def publicado(self):
		ahora = timezone.now()
		return self.filter(

			playlist__stado = PublishStateOptions.PUBLISH,
			playlist__tiempo_publicado__lte=ahora,
			video__stado = PublishStateOptions.PUBLISH,
			video__tiempo_publicado__lte=ahora

		)

class PlayListItemManager(models.Manager):
	def get_queryset(self):
		return PlaylistaItemQueryset(self.model, using=self._db)

	def publicado(self):
		return self.get_queryset().publicado()

class PlayListItem(models.Model):
	playlist = models.ForeignKey(PlayList, on_delete=models.CASCADE)
	video = models.ForeignKey(Video, on_delete=models.CASCADE)
	order = models.IntegerField(default=1)
	timestamp = models.DateTimeField(auto_now_add=True)
	
	objects = PlayListItemManager()

	class Meta:
		ordering = ['order', '-timestamp']

def pr_opcion_limite():
	return Q(type=PlayList.PlaylistTypeChoices.MOVIE) | Q(type=PlayList.PlaylistTypeChoices.SHOW)


class PlayListRelacionado(models.Model):
	playlist = models.ForeignKey(PlayList, on_delete=models.CASCADE)
	relacionado = models.ForeignKey(PlayList, on_delete=models.CASCADE, related_name='item_relacionado', limit_choices_to=pr_opcion_limite)
	order = models.IntegerField(default=1)
	timestamp = models.DateTimeField(auto_now_add=True)

class PeliculaProxyManager(PlayListaManager):
	def all(self):
		return self.get_queryset().filter(type=PlayList.PlaylistTypeChoices.MOVIE)

class MovieProxy(PlayList):

	objects = PeliculaProxyManager()

	def get_video_id(self):
		if self.video is None:
			return None
		return self.video.get_video_id()

	def get_clips(self):
		return self.playlistitem_set.all().publicado()

	class Meta:
		verbose_name= 'Pelicula'
		verbose_name_plural = 'Peliculas'
		proxy = True 

	def save(self, *args, **kwargs):
		self.type = PlayList.PlaylistTypeChoices.MOVIE 
		super().save(*args, **kwargs)



class TVShowProxyManager(PlayListaManager):
	def all(self):
		return self.get_queryset().filter(padre__isnull=True, type=PlayList.PlaylistTypeChoices.SHOW)


class TVShowProxy(PlayList):

	objects = TVShowProxyManager()

	class Meta:
		verbose_name = 'Tv Show'
		verbose_name_plural = 'Tv Shows'
		proxy = True


	def save(self, *args, **kwargs):
		self.type = PlayList.PlaylistTypeChoices.SHOW
		super().save(*args, **kwargs)


	@property 
	def temporada(self):
		return self.playlist_set.publicado()

	def get_corto_display(self):
		return f'{self.temporada.count()} '


class TVShowTemporadaProxyManager(PlayListaManager):
	def all(self):
		return self.get_queryset().filter(padre__isnull=False,  type=PlayList.PlaylistTypeChoices.SEASON)

class TVShowTemporadaProxy(PlayList):

	objects = TVShowTemporadaProxyManager()

	class Meta:
		verbose_name = 'Temporada'
		verbose_name_plural = 'Temporadas'
		proxy = True


	def save(self, *args, **kwargs):
		self.type = PlayList.PlaylistTypeChoices.SEASON
		super().save(*args, **kwargs)


	def get_episodios(self):
		"""
		Obtener episodios para renderizarlos a los usuarios
		"""

		qs = self.playlistitem_set.all().publicado()
		print(qs)
		return qs

pre_save.connect(publicado_stado_pre_save, sender=PlayList)
pre_save.connect(slugify_pre_save, sender=PlayList)

pre_save.connect(publicado_stado_pre_save, sender=MovieProxy)
pre_save.connect(slugify_pre_save, sender=MovieProxy)


pre_save.connect(publicado_stado_pre_save, sender=TVShowProxy)
pre_save.connect(slugify_pre_save, sender=TVShowProxy)


