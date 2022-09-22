from dgf.models import Friend


def update_friend_fields(fields, friends):
    for username, values in friends.items():
        _, created = Friend.objects.update_or_create(username=username, defaults=dict(zip(fields, values)))
        if created:
            print(f'ERROR: Something wrong happened, Friend with username \'{username}\' should exist already!')
