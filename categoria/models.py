from django.contrib.contenttypes.fields import GenericRelation

from django.db import models
from tags.models import TaggedItem

from django.db.models.signals import pre_save

from NetFlix.db.receivers import slugify_pre_save

class categoria(models.Model):
	titulo = models.CharField(max_length=220)
	slug = models.SlugField(blank=True, null=True)
	activo = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	update = models.DateTimeField(auto_now=True)
	tags = GenericRelation(TaggedItem, related_query_name='categoria')



	def get_absolute_url(self):
		return f"/{self.slug}"

	def __str__(self):
		return self.titulo


	class Meta:
		verbose_name= 'Categoria'
		verbose_name_plural='Categorias'


pre_save.connect(slugify_pre_save, sender=categoria)