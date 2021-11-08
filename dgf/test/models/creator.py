from datetime import date

from dgf.models import Course, Friend, Disc, Tournament


def create_objects(type, generator, amount=1):
    type.objects.all().delete()
    objects = [generator(i) for i in range(amount)]
    return objects[0] if len(objects) == 1 else objects


def create_friends(amount=1):
    return create_objects(Friend,
                          lambda i: Friend.objects.create(username=f'friend_{i}',
                                                          first_name=f'Friend{i}'),
                          amount)


def create_courses(amount=1):
    return create_objects(Course,
                          lambda i: Course.objects.create(name=f'Course{i}', udisc_id=f'{i}{i}{i}{i}'),
                          amount)


def create_discs(amount=1):
    return create_objects(Disc,
                          lambda i: Disc.objects.create(mold=f'Disc{i}'),
                          amount)


def create_tournaments(amount=1):
    return create_objects(Tournament,
                          lambda i: Tournament.objects.create(name=f'Tournament{i}',
                                                              begin=date(day=1, month=1, year=2020),
                                                              end=date(day=1, month=1, year=2020)),
                          amount)
