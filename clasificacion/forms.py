
from django import forms

from .models import ClasificacionChoices

class ClasificacionForm(forms.Form):
	clasificacion = forms.ChoiceField(choices=ClasificacionChoices.choices)
	object_id = forms.IntegerField(widget=forms.HiddenInput)
	content_type_id = forms.IntegerField(widget=forms.HiddenInput)
	siguiente = forms.CharField(widget=forms.HiddenInput)
