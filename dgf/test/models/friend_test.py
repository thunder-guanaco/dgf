from django.test import TestCase

from ...models import Friend


class FriendModelTest(TestCase):

    def test_managers(self):
        Friend.objects.all().delete()
        Friend.objects.create(username='manolo')
        Friend.objects.create(username='fede', is_active=True)
        Friend.objects.create(username='kermit', is_active=False)
        self.assertEqual(self.get_usernames(Friend.objects), {'manolo', 'fede'})
        self.assertEqual(self.get_usernames(Friend.all_objects), {'manolo', 'fede', 'kermit'})
        self.assertEqual(self.get_usernames(Friend.non_friends), {'kermit'})

    def get_usernames(self, manager):
        return set(manager.all().values_list('username', flat=True))

    def test_representation(self):
        self.assert_field('__str__', expected='Manuel García García #111828',
                          username='manolo', first_name='Manuel', last_name='García García', pdga_number=111828)
        self.assert_field('__str__', expected='Marcel Knieper',
                          username='marcelk', first_name='Marcel', last_name='Knieper')
        self.assert_field('__str__', expected='Chris #194664',
                          username='chris', first_name='Chris', last_name='', pdga_number=194664)
        self.assert_field('__str__', expected='David',
                          username='davidb', first_name='David', last_name='')
        self.assert_field('__str__', expected='Ricky Wysocki (not DGF)',
                          username='ricky-wysocki', first_name='Ricky', last_name='Wysocki', is_active=False)
        self.assert_field('__str__', expected='Kermit (not DGF)',
                          username='kermit', first_name='Kermit', last_name='', is_active=False)

    def test_full_name(self):
        self.assert_field('full_name', expected='Manuel García García (Manolo)',
                          username='manolo', first_name='Manuel', last_name='García García', nickname='Manolo')
        self.assert_field('full_name', expected='David Strott',
                          username='david', first_name='David', last_name='Strott', nickname=None)

    def test_short_name(self):
        self.assert_field('short_name', expected='Manolo',
                          username='manolo', first_name='Manuel', last_name='García García', nickname='Manolo')
        self.assert_field('short_name', expected='David',
                          username='david', first_name='David', last_name='Strott', nickname=None)

    def test_initials(self):
        self.assert_field('initials', expected='F S',
                          username='fede', first_name='Federico José', last_name='Sörenson Sánchez')
        self.assert_field('initials', expected='M G',
                          username='manolo', first_name='Manuel', last_name='García García')
        self.assert_field('initials', expected='D S',
                          username='david', first_name='David', last_name='Strott')
        self.assert_field('initials', expected='D',
                          username='david', first_name='David', last_name='')

    def test_slug(self):
        self.assert_field('slug', expected='antonio123',
                          username='antonio123')

        self.assert_field('slug', expected='antonio',
                          username='antonio123', first_name='Antonio')

        self.assert_field('slug', expected='tono',
                          username='antonio123', nickname='Toño')
        self.assert_field('slug', expected='tono',
                          username='antonio123', first_name='Antonio', nickname='Toño')

        self.assert_field('slug', expected='tony',
                          username='antonio123', slug='tony')
        self.assert_field('slug', expected='tony',
                          username='antonio123', first_name='Antonio', slug='tony')
        self.assert_field('slug', expected='tony',
                          username='antonio123', nickname='Toño', slug='tony')
        self.assert_field('slug', expected='tony',
                          username='antonio123', first_name='Antonio', nickname='Toño', slug='tony')

    def assert_field(self, what, expected, **fields):
        Friend.objects.all().delete()
        friend = Friend(**fields)
        friend.save()
        actual = str(friend) if what == '__str__' else getattr(friend, what)
        self.assertEqual(actual, expected)
