from django.test import TestCase

from django.utils import timezone
from django.utils.text import slugify

from NetFlix.db.models import PublishStateOptions

from Video.models import Video
from .models import PlayList

from django.conf import settings

from .models import PlayList, MovieProxy, TVShowProxy

#python manage.py dumpdata playlist > playlist.json
#python manage.py dumpdata categoria playlist > proj.json
#python manage.py dumpdata categoria playlist Video tags > project.json

class PlayListViewTestCase(TestCase):
	fixtures = ['project']

	def test_queryset_exists(self):
		self.assertTrue(PlayList.objects.exists())


	def test_pelicula_count(self):
		qs = MovieProxy.objects.all()
		self.assertEqual(qs.count(), 0)

	def test_show_count(self):
		qs = TVShowProxy.objects.all()
		self.assertEqual(qs.count(), 1)


	def test_show_detail_view(self):
		show = TVShowProxy.objects.all().publicado().first()
		url = show.get_absolute_url()
		self.assertIsNotNone(url)	
		response = self.client.get(url) #Get Request some url
		self.assertEqual(response.status_code, 200) #200
		self.assertContains(response, f"{show.titulo}")
		#html = response.content
		context = response.context
		obj = context['object']
		self.assertEqual(obj.id, show.id)


	def test_show_detail_redirect_view(self):
		show = TVShowProxy.objects.all().publicado().first()
		url = f"/shows/{show.slug}"
		self.assertIsNotNone(url)	
		response = self.client.get(url, follow=True) #follow=True es para las url no validas
		self.assertEqual(response.status_code, 200) #200


	def test_movie_detail_view(self):
		movie = MovieProxy.objects.all().publicado().first()
		url = movie.get_absolute_url()
		self.assertIsNotNone(url)	
		response = self.client.get(url) #Get Request some url
		self.assertEqual(response.status_code, 200) #200
		self.assertContains(response, f"{movie.titulo}")
		#html = response.content
		context = response.context
		obj = context['object']
		self.assertEqual(obj.id, movie.id)

	def test_movie_detail_view(self):
		movie = MovieProxy.objects.all().publicado().first()
		url = f"/movies/{movie.slug}"
		self.assertIsNotNone(url)	
		response = self.client.get(url, follow=True) #Get Request some url
		self.assertEqual(response.status_code, 200) #200
