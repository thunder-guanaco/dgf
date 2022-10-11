from dgf.models import Division

for division in ['A', 'B', 'C', 'D', 'E']:
    text = f'{division}-Klasse'
    Division.objects.create(id=text, text=text)
