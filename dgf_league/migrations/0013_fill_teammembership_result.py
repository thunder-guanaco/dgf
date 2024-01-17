from django.db import migrations


def fill_team_memberships(apps, schema_editor):
    TeamMembership = apps.get_model('dgf_league', 'TeamMembership')
    TeamMembershipTmp = apps.get_model('dgf_league', 'TeamMembershipTmp')
    for team_membership in TeamMembership.objects.all():
        TeamMembershipTmp.objects.create(team=team_membership.team, friend=team_membership.friend)


def fill_results(apps, schema_editor):
    Result = apps.get_model('dgf_league', 'Result')
    ResultTmp = apps.get_model('dgf_league', 'ResultTmp')
    for result in Result.objects.all():
        ResultTmp.objects.create(match=result.match, team=result.team, points=result.points)


class Migration(migrations.Migration):
    dependencies = [
        ('dgf_league', '0012_resulttmp_teammembershiptmp'),
    ]

    operations = [
        migrations.RunPython(fill_team_memberships),
        migrations.RunPython(fill_results),
    ]
