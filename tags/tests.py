from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.utils import IntegrityError


from django.test import TestCase

from playlist.models import PlayList
from .models import TaggedItem

class TaggedItemTestCase(TestCase):
	def setUpt(self):
		ply_titulo = 'Nuevo Titulo'
		self.ply_obj = PlayList.objects.create(titulo=ply_titulo)
		self.ply_obj2 = PlayList.objects.create(titulo=ply_titulo)
		self.ply_titulo=ply_titulo
		self.ply_obj.tags.add(TaggedItem(tag='nuevo-titulo'), bulk=False)
		self.ply_obj2.tags.add(TaggedItem(tag='nuevo-titulo'), bulk=False)

	def test_content_type_is_not_null(self):
		with self.assertRaises(IntegrityError):
			TaggedItem.objects.create(tag='mi-nuevo-tag')


	def test_crear_via_content_type(self):
		c_type = ContentType.objects.get(app_label='playlist', model='playlist')
		tag_a = TaggedItem.objects.create(content_type=c_type, object_id=1, tag='nuevo-tag')
		self.assertIsNotNone(tag_a.pk)
		tag_a = TaggedItem.objects.create(content_type=c_type, object_id=100, tag='nuevo-tag2')
		self.assertIsNotNone(tag_a.pk)

	def test_crear_via_model_content_type(self):
		c_type = ContentType.objects.get_for_model(PlayList)
		tag_a = TaggedItem.objects.create(content_type=c_type, object_id=1, tag='mi-nuevo-tag')
		self.assertIsNotNone(tag_a.pk)

	def test_crear_via_app_loader_content_type(self):
		PlayListKlass = apps.get_model(app_label='playlist', model_name='PlayList')
		c_type = ContentType.objects.get_for_model(PlayListKlass)
		tag_a = TaggedItem.objects.create(content_type=c_type, object_id=1, tag='mi-nuevo-tag')
		self.assertIsNotNone(tag_a.pk)

	def test_related_field(self):
		self.assertEqual(self.ply_obj.tags.count(), 1)

	def test_related_field_create(self):
		self.ply_obj.tags.create(tag='otro-nuevo-tag')
		self.assertEqual(self.ply_obj.tags.count(), 2)

	def test_related_field_query_name(self):
		qs = TaggedItem.objects.filter(playlist__titulo__iexact=self.ply_titulo)
		self.assertEqual(qs.count(), 2)

	def test_related_field_via_content_type(self):
		c_type = ContentType.objects.get_for_model(PlayList)
		tag_qs = TaggedItem.objects.filter(content_type=c_type, object_id=self.ply_obj.id)
		self.assertEqual(tag_qs.count(), 1)

	def test_direct_obj_created(self):
		obj = self.ply_obj
		tag = TaggedItem.objects.create(content_object=obj, tag='otro1')
		self.assertIsNotNone(tag.pk)
