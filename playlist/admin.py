from django.contrib import admin

from .models import PlayList, PlayListItem, MovieProxy, TVShowProxy, TVShowTemporadaProxy


class MovieProxyAdmin(admin.ModelAdmin):
	list_display = ['titulo']
	fields = ['titulo', 'descripcion', 'stado', 'video', 'slug']
	class Meta:
		model = MovieProxy

	def get_queryset(self, request):
		return MovieProxy.objects.all()

admin.site.register(MovieProxy, MovieProxyAdmin)


class TemporadaEpisodioInline(admin.TabularInline):
	model = PlayListItem
	extra = 0

class TVShowTemporadaProxyAdmin(admin.ModelAdmin):
	inlines = [TemporadaEpisodioInline]
	list_display = ['titulo', 'padre']
	class Meta:
		model = TVShowTemporadaProxy

	def get_queryset(self, request):
		return TVShowTemporadaProxy.objects.all()

admin.site.register(TVShowTemporadaProxy, TVShowTemporadaProxyAdmin)

class TVShowTemporadaProxyInline(admin.TabularInline):
	model = TVShowTemporadaProxy
	extra = 0
	fields= ['order', 'titulo', 'stado']

class TVShowProxyAdmin(admin.ModelAdmin):
	inlines = [TVShowTemporadaProxyInline]
	fields = ['padre', 'titulo', 'stado', 'type', 'descripcion', 'video', 'slug']
	class Meta:
		model = TVShowProxy

	def get_queryset(self, request):
		return TVShowProxy.objects.all()

admin.site.register(TVShowProxy, TVShowProxyAdmin)

class PlayListItemInline(admin.TabularInline):
	model = PlayListItem
	extra = 0


class PlayListAdmin(admin.ModelAdmin):
	inlines = [PlayListItemInline]
	class Meta:
		model = PlayList

	def get_queryset(self, request):
		return PlayList.objects.filter(type=PlayList.PlaylistTypeChoices.PLAYLIST)

admin.site.register(PlayList, PlayListAdmin)
admin.site.register(PlayListItem)