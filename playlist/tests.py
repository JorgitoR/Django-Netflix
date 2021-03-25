from django.test import TestCase

from NetFlix.db.models import PublishStateOptions
from .models import PlayList
from Video.models import Video 
from django.utils.text import slugify

class PlaylistModelTestCase(TestCase):

	def crear_video(self):
		video_a = Video.objects.create(titulo='My title', video_id='abc123')
		video_b = Video.objects.create(titulo='My title', video_id='abc1233')
		video_c = Video.objects.create(titulo='My title', video_id='abc1234')
		self.video_a = video_a
		self.video_b = video_b
		self.video_c = video_c
		self.video_qs = Video.objects.all()

	def setUp(self):
		self.crear_video()
		#self.video_a = video_a
		self.obj_a = PlayList.objects.create(titulo='este es mi titulo', video=self.video_a)
		obj_b = PlayList.objects.create(titulo='este es mi titulo', 
								stado=PublishStateOptions.PUBLISH,
		 						video=self.video_a)

		# obj_b.videos.set([self.video_a, self.video_b, self.video_c])
		obj_b.videos.set(self.video_qs)
		obj_b.save()

		self.obj_b = obj_b

	def test_playlist_video(self):
		self.assertEqual(self.obj_a.video, self.video_a)

	def test_video_playlist_ids_propery(self):
		ids = self.obj_a.video.get_playlista_ids()
		actual_ids = list(PlayList.objects.filter(video=self.video_a).values_list('id', flat=True))
		self.assertEqual(ids, actual_ids)

	def test_video_playlist(self):
		qs = self.video_a.playlist_destacado.all()
		self.assertEqual(qs.count(), 2)

	def test_playlist_video_through_model(self):
		v_qs = sorted(list(self.video_qs.values_list('id')))
		video_qs = sorted(list(self.obj_b.videos.all().values_list('id')))
		playlist_item_qs = sorted(list(self.obj_b.playlistitem_set.all().values_list('video')))
		self.assertEqual(v_qs, video_qs, playlist_item_qs)

	def test_slug_field(self):
		titulo = self.obj_a.titulo
		test_slug = slugify(titulo)
		self.assertEqual(test_slug, self.obj_a.slug)
