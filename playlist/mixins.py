class PlayListMixin():
	template_name = 'playlist_lista.html'
	titulo = None

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
	
		if self.titulo is not None:
			context['titulo'] = self.titulo
		return context

	def get_queryset(self):
		return super().get_queryset().publicado()