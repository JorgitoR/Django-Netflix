from django.db import models


from django.contrib.contenttypes.models import ContentType 
from django.contrib.contenttypes.fields import GenericForeignKey 

from django.db.models.signals import pre_save

class TaggItemManager(models.Manager):
	def lista_unica(self):
		tags_set = set(self.get_queryset().values_list('tag', flat=True))
		tags_list = sorted(list(tags_set))
		return tags_list

class TaggedItem(models.Model):
	tag = models.SlugField()
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey("content_type", "object_id")

	objects = TaggItemManager()
	

	def __str__(self):
		return self.tag

	@property 
	def slug(self):
		return self.tag
	
    # def get_related_object(self):
    #     Klass = self.content_type.model_class()
    #     return Klass.objects.get(id=self.object_id)


def tag_minuscula_pre_save(sender, instance, *args, **kwargs):
	instance.tag = f"{instance.tag}".lower()


pre_save.connect(tag_minuscula_pre_save, sender=TaggedItem)