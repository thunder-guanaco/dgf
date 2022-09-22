from pprint import pprint

from dgf.models import Friend

pprint(list(Friend.objects.all()
            .values_list('username', 'pdga_number', 'gt_number', 'udisc_username', 'metrix_user_id')
            .order_by('username')
            )
       )
