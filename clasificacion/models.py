from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Avg
from django.db.models.signals import pre_save, post_save

from django.db import models

User = settings.AUTH_USER_MODEL

class ClasificacionChoices(models.IntegerChoices):
	UNO = 1
	DOS = 2
	TRES = 3
	CUATRO = 4
	CINCO = 5

	__empty__='Clasifica esto'


class ClasificacionQuerySet(models.QuerySet):
	def rating(self):
		return self.aggregate(average=Avg("valor"))['average']


class ClasificacionManager(models.Manager):
	def get_queryset(self):
		return ClasificacionQuerySet(self.model, using=self._db)

class Clasificacion(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	valor = models.IntegerField(null=True, blank=True, choices=ClasificacionChoices.choices)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey("content_type", "object_id")


	objects = ClasificacionManager()


def clasificacion_post_save(sender, instance, *args, **kwargs):
	if created:
		content_type = instance.content_type
		usuario = instance.usuario
		qs = Clasificacion.objects.filter(
				usuario=usuario, 
				content_type=content_type,
				object_id=instance.object_id).exclude(pk=instance.pk)

		if qs.exists():
			qs.delete()


post_save.connect(clasificacion_post_save, sender=Clasificacion)
