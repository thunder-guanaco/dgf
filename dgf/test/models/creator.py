from datetime import date, datetime

from dgf.models import Course, Friend, Disc, Tournament, Division, BagTagChange, GitHubIssue, Tour


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


def create_bag_tag_changes(amount=1):
    friend, _ = Friend.objects.get_or_create(username='friend_x')
    return create_objects(BagTagChange,
                          lambda i: BagTagChange.objects.create(actor=friend,
                                                                friend=friend,
                                                                new_number=i,
                                                                previous_number=10,
                                                                timestamp=datetime.now()),
                          amount)


def create_git_hub_issues(amount=1):
    return create_objects(GitHubIssue,
                          lambda i: GitHubIssue.objects.create(title=f'GitHub Issue {i}'),
                          amount)


def create_tours(amount=1):
    return create_objects(Tour,
                          lambda i: Tour.objects.create(name=f'Tour {i}'),
                          amount)


def create_divisions():
    Division.objects.all().delete()
    Division.objects.create(id='MPO', text='MPO - Pro Open')
    Division.objects.create(id='FPO', text='FPO - Pro Open Women')
    Division.objects.create(id='MA1', text='MA1 - Advanced')
    Division.objects.create(id='MA2', text='MA2 - Intermediate')
    Division.objects.create(id='MA3', text='MA3 - Recreational')
    Division.objects.create(id='MA4', text='MA4 - Novice')
