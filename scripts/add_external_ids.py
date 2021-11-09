from dgf.models import Friend

friends = [
    # username, PDGA, GT, Udisc, Metrix
    ('alex', 126231, 1436, 'alexso', '62515'),
    ('angela', 147164, 2129, 'aceangie', '55028'),
    ('armin', 147160, 2127, 'putterbomb', '54515'),
    ('chris', 194664, X, 'chaberno', '112752'),
    ('david', 82985, 1711, 'davido', '20851'),
    ('fede', 109371, 2106, 'fedejsoren', '39904'),
    ('hilde', 56334, X, 'chrishilde', '25850'),
    ('ilija', 104565, 2040, 'ilimiha', '26762'),
    ('jogi', 125551, 1847, 'jogi4711', '25547'),
    ('julia', 144087, 2237, 'julest', '54522'),
    ('justus', 111413, 2118, 'justusfriedrich', '48541'),
    ('jutta', 129326, 828, 'juttawenner', '24088'),
    ('kevin', 47163, 427, 'kevinkonsorr', '25994'),
    ('lux', 71666, 1582, 'lux', '54523'),
    ('manolo', 111828, 1922, 'manologg', '25533'),
    ('marcel', 110666, 2119, 'selloh', '44175'),
    ('marcelr', X, X, X, '92056'),
    ('marian', 112270, 2110, 'marian', '39303'),
    ('mario', 115250, 2121, 'mariofriedrich', '48542'),
    ('markus', 94728, 1841, 'markustm', '25538'),
    ('matthias', 147730, 2488, 'thias87', '53833'),
    ('michael', 47164, X, 'michael3001', '90199'),
    ('paul', 125227, 2327, 'paulgi', '42852'),
    ('ralf', 91363, X, 'rollerralf', '41591'),
    ('ralfw', 104566, X, 'rallewi', '26806'),
    ('tobias', 127232, 2396, 'nr127232', '68205'),
    ('uli', 77646, 1769, 'ulrichberg', '23739'),

    # non-PDGA members
    ('davidb', None, X, 'gerbeerserker', '129951'),
    ('helge', None, X, 'gmstrott', '116149'),
    ('jesko', None, X, 'JeKo', '116360'),
    ('lennard', None, X, 'Lennardowski', '114206'),
    ('marcelk', None, X, 'marcelge91', '113505'),
    ('markuss', None, X, 'cardenalmendoza', '114204'),
    ('tana', None, X, 'tanapat', '101826'),

    # supporting members
    ('babara', None, None, None, None),
    ('basti', None, None, None, None),
    ('bettina', None, None, None, None),
    ('conni', None, None, None, None),
    ('dorina', None, None, None, None),
    ('julia-sophie', None, None, None, None),
    ('louis', None, None, None, None),
    ('oma', None, None, None, None),
    ('stefanie', None, None, None, None),
    ('stephan', None, None, None, None),
    ('uwe', None, None, None, None),
    ('wolfgang', None, None, None, None),
    ('zinnia', None, None, None, None),
]

for username, pdga_number, gt_number, udisc_username, metrix_user_id in friends:
    try:
        friend = Friend.objects.get(username=username)
        if pdga_number:
            friend.pdga_number = pdga_number
        if gt_number:
            friend.gt_number = gt_number
        if udisc_username:
            friend.udisc_username = udisc_username
        if metrix_user_id:
            friend.metrix_user_id = metrix_user_id
        friend.save()
    except Friend.DoesNotExist:
        print(f'ERROR: Friend with username \'{username}\' does not exist!')
