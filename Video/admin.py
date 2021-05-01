from django.contrib import admin
from .models import Video, ProxiTodoLosVideo, VideoPublicadoProxy

class VideoAdmin(admin.ModelAdmin):
	list_display = ['titulo', 'id', 'stado', 'video_id', 'es_publicado', 'get_playlista_ids']
	search_fields = ['titulo']
	list_filter=['stado', 'activo']
	readonly_fields= ['id', 'timestamp', 'es_publicado', 'tiempo_publicado', 'get_playlista_ids']

	class Meta:
		model = ProxiTodoLosVideo


admin.site.register(Video, VideoAdmin)

class VideoPublicadoProxyAdmin(admin.ModelAdmin):

	list_display = ['titulo', 'video_id']
	search_fields = ['titulo']

	class Meta:
		model = VideoPublicadoProxy

	def get_queryset(self, request):
		return ProxiTodoLosVideo.objects.filter(activo=True)


admin.site.register(VideoPublicadoProxy, VideoPublicadoProxyAdmin)