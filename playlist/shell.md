


python manage.py shell

from Video.models import Video

obj = Video.objects.get(id='2')
dir(obj)

qs = Video.objects.all()
qs.order_by("-timestamp")

