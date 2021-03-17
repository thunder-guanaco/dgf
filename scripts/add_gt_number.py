from dgf.models import Friend

friends = [
    ('alex', 1436),
    ('angela', 2129),
    ('armin', 2127),
    ('babara', None),
    ('basti', None),
    ('bettina', None),
    ('conni', None),
    ('david', 1711),
    ('dorina', None),
    ('fede', 2106),
    ('helge', None),
    ('ilija', 2040),
    ('jogi', 1847),
    ('julia', 2237),
    ('julia-sophie', None),
    ('justus', 2118),
    ('jutta', 828),
    ('kevin', 427),
    ('louis', None),
    ('lux', 1582),
    ('manolo', 1922),
    ('marcel', 2119),
    ('marcelr', None),
    ('marian', 2110),
    ('mario', 2121),
    ('markus', 1841),
    ('matthias', 2488),
    ('oma', None),
    ('paul', 2327),
    ('ralf', None),
    ('stefanie', None),
    ('stephan', None),
    ('tobias', 2396),
    ('uli', 1769),
    ('uwe', None),
    ('wolfgang', None),
    ('zinnia', None)
]

for username, gt_number in friends:
    friend = Friend.objects.get(username=username)
    friend.gt_number = gt_number
    friend.save()
