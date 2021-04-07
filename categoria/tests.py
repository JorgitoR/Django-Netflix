from django.test import TestCase

from .models import categoria
from playlist.models import PlayList

class CategoriaTestCase(TestCase):
	def setUp(self):
		categoria_a = categoria.objects.create(titulo='Acion')
		categoria_b = categoria.objects.create(titulo='Comedia', activo=False)
		self.play_a = PlayList.objects.create(titulo='Este es mi titulo', categoria=categoria_a)
		self.categoria_a = categoria_a
		self.categoria_b = categoria_b


	def test_esta_activo(self):
		self.assertTrue(self.categoria_a.activo)

	def  test_no_esta_activo(self):
		self.assertFalse(self.categoria_b.activo)

	def test_relacion_playlist(self):
		qs = self.categoria_a.playlist.all()
		self.assertEqual(qs.count(), 1)