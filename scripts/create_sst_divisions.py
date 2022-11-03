from dgf.models import Division

for division in ['RAE', 'RAF', 'OR', 'R900']:
    division, _ = Division.objects.get_or_create(id=division)
    division.text = division.id
    division.save()
