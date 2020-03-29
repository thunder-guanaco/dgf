import cronjobs
from django_cron import CronJobBase, Schedule

from .models import Friend
from .pdga import PdgaApi


@cronjobs.register
class PdgaFetcher(CronJobBase):
    RUN_EVERY_MINS = 240  # every 4 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'dgf.pdga'

    def do(self):
        pdga_service = PdgaApi()
        for friend in Friend.objects.all():
            if friend.pdga_number:
                pdga_friend_response = pdga_service.query_player(pdga_number=friend.pdga_number)
                friend.rating = int(pdga_friend_response['players'][0]['rating'])
                friend.save()
