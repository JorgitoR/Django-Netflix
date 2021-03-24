from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify
from .models import Video

from NetFlix.db.models import PublishStateOptions

class VideoModelTestCase(TestCase):
	def setUp(self): #es importante escribir setUp de lo contrario no funcionara
		self.obj_a = Video.objects.create(titulo="Hi mundo", video_id='abc')
		self.obj_b = Video.objects.create(titulo="Hi mundo", video_id='abc2', stado=PublishStateOptions.PUBLISH)

	def test_slug_field(self):
		titulo = self.obj_a.titulo
		test_slug = slugify(titulo)
		self.assertEqual(test_slug, self.obj_a.slug)

	def test_valido_titulo(self): #siempre comienza con test_
		titulo = "Hi mundo"
		qs = Video.objects.filter(titulo=titulo)
		self.assertTrue(qs.exists())

	def test_crear_contador(self):
		titulo ="Hi mundo"
		qs = Video.objects.all()
		self.assertEqual(qs.count(), 2)

	def test_draft_case(self):
		qs = Video.objects.filter(stado=PublishStateOptions.DRAFT)
		self.assertEqual(qs.count(), 1)


	def test_publish_case(self):
		qs = Video.objects.filter(stado=PublishStateOptions.PUBLISH)
		ahora = timezone.now()
		publicado_qs = Video.objects.filter(tiempo_publicado__lte=ahora)
		self.assertTrue(publicado_qs.exists())


	def test_publicado_manager(self):
		publicado_qs = Video.objects.all().publicado()
		publicado_qs2 = Video.objects.publicado()
		self.assertTrue(publicado_qs.exists())
		self.assertEqual(publicado_qs.count(), publicado_qs2.count())