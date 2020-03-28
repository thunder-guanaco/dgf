import cronjobs

from .models import Friend
from .pdga import PdgaApi


# @cronjobs.register
def fill_friends_data():
    pdga_service = PdgaApi()

    friend = Friend()
    friend.pdga_number = 109371

    # ~for friend in Friend.objects.all():
    if friend.pdga_number:
        pdga_friend_response = pdga_service.query_player(pdga_number=friend.pdga_number)
        friend.rating = pdga_friend_response['players'][0]['rating']
        friend.save()


fill_friends_data()
