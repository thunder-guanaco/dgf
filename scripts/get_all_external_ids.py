from dgf.models import Friend


def str_or_none(attribute):
    return f'\'{attribute}\'' if attribute else 'None'


def print_friend(friend):
    print(f'    \'{friend.username}\': [{friend.pdga_number}, {friend.gt_number}, '
          f'{str_or_none(friend.udisc_username)}, {str_or_none(friend.metrix_user_id)}],')


def print_friends(friends, comment=None):
    print('')
    if comment:
        print(f'    # {comment}')
    for friend in friends:
        print_friend(friend)


all_filled = []
non_pdga = []
non_gt = []
non_udisc = []
non_metrix = []
supporting = []
incomplete = []
for f in Friend.objects.all().order_by('username'):

    if f.pdga_number and f.gt_number and f.udisc_username and f.metrix_user_id:
        all_filled.append(f)

    elif not f.pdga_number and f.gt_number and f.udisc_username and f.metrix_user_id:
        non_pdga.append(f)

    elif f.pdga_number and not f.gt_number and f.udisc_username and f.metrix_user_id:
        non_gt.append(f)

    elif f.pdga_number and f.gt_number and not f.udisc_username and f.metrix_user_id:
        non_udisc.append(f)

    elif f.pdga_number and f.gt_number and f.udisc_username and not f.metrix_user_id:
        non_metrix.append(f)

    elif not f.pdga_number and not f.gt_number and not f.udisc_username and not f.metrix_user_id:
        supporting.append(f)

    else:
        incomplete.append(f)

print_friends(all_filled)
print_friends(non_pdga, comment='non-PDGA')
print_friends(non_gt, comment='non-GT')
print_friends(non_udisc, comment='non-UDisc')
print_friends(non_metrix, comment='non-Metrix')
print_friends(incomplete, comment='incomplete')
print_friends(supporting, comment='supporting')
