from dgf.models import Friend

friends = [
    # username, PDGA, GT, Udisc, Metrix
    ('alex', 126231, 1436, 'alexso', 62515),
    ('angela', 147164, 2129, 'aceangie', 55028),
    ('armin', 147160, 2127, 'putterbomb', 54515),
    ('babara', None, None, None, None),
    ('basti', None, None, None, None),
    ('bettina', None, None, None, None),
    ('chris', 194664, None, None, 112752),
    ('conni', None, None, None, None),
    ('david', 82985, 1711, 'davido', 20851),
    ('davidb', None, None, None, 129951),
    ('dorina', None, None, None, None),
    ('fede', 109371, 2106, 'fedejsoren', 39904),
    ('helge', None, None, None, 116149),
    ('hilde', None, None, None, 25850),
    ('ilija', 104565, 2040, 'ilimiha', 26762),
    ('jesko', None, None, 'JeKo', 116360),
    ('jogi', 125551, 1847, 'jogi4711', 25547),
    ('julia', 144087, 2237, 'julest', 54522),
    ('julia-sophie', None, None, None, None),
    ('justus', 111413, 2118, 'justusfriedrich', 48541),
    ('jutta', 129326, 828, None, 24088),
    ('kevin', 47163, 427, 'kevinkonsorr', 25994),
    ('lennard', None, None, None, 114206),
    ('louis', None, None, None, None),
    ('lux', 71666, 1582, 'lux', 54523),
    ('manolo', 111828, 1922, 'manologg', 25533),
    ('marcel', 110666, 2119, 'selloh', 44175),
    ('marcelk', None, None, None, 113505),
    ('marcelr', None, None, None, 92056),
    ('marian', 112270, 2110, 'marian', 39303),
    ('mario', 115250, 2121, 'mariofriedrich', 48542),
    ('markus', 94728, 1841, 'markustm', 25538),
    ('markuss', None, None, None, 114204),
    ('matthias', 147730, 2488, 'thias87', 53833),
    ('michael', 47164, None, None, 90199),
    ('oma', None, None, None, None),
    ('paul', 125227, 2327, 'paulgi', 42852),
    ('ralf', 91363, None, 'rollerralf', 41591),
    ('ralfw', 104566, None, None, 26806),
    ('stefanie', None, None, None, None),
    ('stephan', None, None, None, None),
    ('tana', None, None, None, 101826),
    ('tobias', 127232, 2396, 'nr127232', 68205),
    ('uli', 77646, 1769, None, 23739),
    ('uwe', None, None, None, None),
    ('wolfgang', None, None, None, None),
    ('zinnia', None, None, None, None),
]

for username, pdga_number, gt_number, udisc_username, metrix_user_id in friends:
    try:
        friend = Friend.objects.get(username=username)
        friend.pdga_number = pdga_number
        friend.gt_number = gt_number
        friend.udisc_username = udisc_username
        friend.metrix_user_id = metrix_user_id
        friend.save()
    except Friend.DoesNotExist:
        print(f'ERROR: Friend with username \'{username}\' does not exist!')
