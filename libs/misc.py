
# Remove model items > 30 minutes old
from datetime import timedelta
from django.utils import timezone

# https://stackoverflow.com/questions/37607411/django-runtimewarning-datetimefield-received-a-naive-datetime-while-time-zon/37607525
def cleanup(model) :
    time_threshold = timezone.now() - timedelta(minutes=30)
    count = model.objects.filter(created_at__lt=time_threshold).count()
    # print('Found',count,'expired', model._meta.verbose_name)
    if count > 0 :
        model.objects.filter(created_at__lt=time_threshold).delete()
        print('Deleted',count,'expired', model._meta.verbose_name)

