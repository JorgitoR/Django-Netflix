from django.test import TestCase

import random
from django.contrib.auth import get_user_model
from django.db.models import Avg

from playlist.models import PlayList 
from .models import ClasificacionChoices, Clasificacion

User = get_user_model()

class ClasificacionTestCase(TestCase):
	def crear_playlista(self):
		items = []
		self.playlist_contador = random.randint(10, 500)
		for i in range(0, self.playlist_contador):
			items.append(PlayList(titulo=f'Tv Show {i}'))

		PlayList.objects.bulk_create(items)
		self.playlist = PlayList.objects.all()


	def crear_usuarios(self):
		items = []
		self.usuario_contador = random.randint(10, 500)
		for i in range(0, self.usuario_contador):
			items.append(User(username=f'user_{i}'))
		User.objects.bulk_create(items)
		self.usuarios = User.objects.all()


	def crear_clasificacion(self):
		items = []
		self.clasificacion_total = []
		self.clasificacion_contador = 1_000
		for i in range(0, self.clasificacion_contador):
			usuario_obj = self.usuarios.order_by("?").first()
			ply_obj = self.playlist.order_by("?").first()
			clasificacion_valor = random.choice(ClasificacionChoices.choices)[0]
			if clasificacion_valor is not None:
				self.clasificacion_total.append(clasificacion_valor)

			items.append(
				Clasificacion(

					usuario = usuario_obj, 
					content_object = ply_obj, 
					valor = clasificacion_valor
				)
			)

			Clasificacion.objects.bulk_create(items)
			self.clasificacion = Clasificacion.objects.all()

	def setUp(self):
		self.crear_playlista()
		self.crear_usuarios()
		self.crear_clasificacion()


	def test_usuario_contador(self):
		qs = User.objects.all()
		self.assertTrue(qs.exists())
		self.assertEqual(qs.count(), self.usuario_contador)
		self.assertEqual(self.usuarios.count(), self.usuario_contador)


	def test_playlist_contador(self):
		qs = PlayList.objects.all()
		self.assertTrue(qs.exists())
		self.assertEqual(qs.count(), self.playlist_contador)
		self.assertEqual(self.playlist.count(), self.playlist_contador)

	def test_clasificacion_contador(self):
		qs = Clasificacion.objects.all()
		self.assertTrue(qs.exists())
		self.assertEqual(qs.count(), self.clasificacion_contador)
		self.assertEqual(self.clasificacion.count(), self.clasificacion_contador)


	def test_clasificacion_random_choices(self):
		valor_set = set(Clasificacion.objects.values_list('value', flat=True))
		self.assertTrue(len(valor_set) > 1)


	def test_clasificacion_agg(self):
		db_avg = Clasificacion.objects.aggregate(average=Avg('valor'))['average']
		self.assertIsNotNone(db_avg)
		self.assertTrue(db_avg > 0)
		total_sum = sum(self.clasificacion_total)
		passed_avg = total_sum / (len(self.clasificacion_total) * 1.0)
		print(db_avg, passed_avg)
		self.assertEqual(db_avg, passed_avg)

	def test_clasificacion_playlist_avg(self):
		item_1 = PlayList.objects.aggregate(average=Avg('clasificacion__valor'))['average']
		self.assertIsNotNone(item_1)
		self.assertTrue(item_1 > 0)