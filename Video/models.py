from django.db import models

from django.utils import timezone
from django.utils.text import slugify

from django.db.models.signals import pre_save

from NetFlix.db.models import PublishStateOptions
from NetFlix.db.receivers import publicado_stado_pre_save, slugify_pre_save


class VideoQuerySet(models.QuerySet):
	def publicado(self):
		ahora = timezone.now()
		return self.filter(
			stado = PublishStateOptions.PUBLISH,
			tiempo_publicado__lte=ahora
		)


class VideoManager(models.Manager):
	def get_queryset(self):
		return VideoQuerySet(self.model, using=self._db)

	def publicado(self):
		return self.get_queryset().publicado()


class Video(models.Model):

	titulo = models.CharField(max_length=120)
	descripcion = models.TextField(blank=True, null=True)
	slug = models.SlugField(blank=True, null=True)
	activo = models.BooleanField(default=True)
	video_id = models.CharField(max_length=120, unique=True)

	timestamp = models.DateTimeField(auto_now_add=True)
	update = models.DateTimeField(auto_now=True)

	stado = models.CharField(max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)

	tiempo_publicado = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

	objects = VideoManager()

	def __str__(self):
		return self.titulo

	def get_video_id(self):
		if not self.es_publicado:
			return None
		return self.video_id

	def get_descripcion_trailer(self):
		return self.descripcion

	@property
	def es_publicado(self):
		if self.activo is False:
			return False
		estado = self.stado
		if estado != PublishStateOptions.PUBLISH:
			return False
		tiempo_publicado = self.tiempo_publicado
		if tiempo_publicado is None:
			return False
		ahora = timezone.now()
		return tiempo_publicado <= ahora

	def get_playlista_ids(self):
		#self.<foreingkey_obj>_set.all()
		#return list(self.playlist_set.all().values_list('id', flat=True))playlist_destacado
		return list(self.playlist_destacado.all().values_list('id', flat=True))

	#def save(self, *args, **kwargs):
	#	if self.stado == self.PublishStateOptions.PUBLISH and self.tiempo_publicado is None:
	#		print("Guardado el tiempo de publicado")
	#		self.tiempo_publicado = timezone.now()

	#	elif self.stado == self.PublishStateOptions.DRAFT:
	#		self.tiempo_publicado = None
	#	if self.slug is None:
	#		self.slug = slugify(self.titulo)
	#	super().save(*args, **kwargs)

class ProxiTodoLosVideo(Video):
	class Meta:
		proxy = True
		verbose_name = "Todo los Video"
		verbose_name_plural="Todos los Publicados"

class VideoPublicadoProxy(Video):
	class Meta:
		proxy =True
		verbose_name ='Video Publicado'
		verbose_name_plural = 'Videos Publicados'

pre_save.connect(publicado_stado_pre_save, sender=Video)
pre_save.connect(slugify_pre_save, sender=Video)

pre_save.connect(publicado_stado_pre_save, sender=ProxiTodoLosVideo)
pre_save.connect(slugify_pre_save, sender=ProxiTodoLosVideo)

pre_save.connect(publicado_stado_pre_save, sender=VideoPublicadoProxy)
pre_save.connect(slugify_pre_save, sender=VideoPublicadoProxy)

