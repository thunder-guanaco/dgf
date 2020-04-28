from django.test import TestCase

from ..models import Friend, Course, DiscInBag, Disc


class FriendModelTest(TestCase):

    def test_slug(self):
        self.expect_slug('antonio123', username='antonio123')

        self.expect_slug('antonio', username='antonio123', first_name='Antonio')

        self.expect_slug('tono', username='antonio123', nickname='Toño')
        self.expect_slug('tono', username='antonio123', first_name='Antonio', nickname='Toño')

        self.expect_slug('tony', username='antonio123', slug='tony')
        self.expect_slug('tony', username='antonio123', first_name='Antonio', slug='tony')
        self.expect_slug('tony', username='antonio123', nickname='Toño', slug='tony')
        self.expect_slug('tony', username='antonio123', first_name='Antonio', nickname='Toño', slug='tony')

    def expect_slug(self, expected_slug, **fields):
        Friend.objects.all().delete()
        friend = Friend(**fields)
        friend.save()
        self.assertEqual(friend.slug, expected_slug)


class CourseModelTest(TestCase):

    def test_representation(self):
        self.expect_representation(expected='Fröndenberg',
                                   name='Fröndenberg', city='Fröndenberg', country='DE')

        self.expect_representation(expected='Volkspark Potsdam',
                                   name='Volkspark Potsdam', city='Potsdam', country='DE')

        self.expect_representation(expected='Wischlingen (Dortmund)',
                                   name='Wischlingen', city='Dortmund', country='DE')

        self.expect_representation(expected='Mijas (ES)',
                                   name='Mijas', city='Mijas', country='ES')

        self.expect_representation(expected='DiscGolfPark Mijas (ES)',
                                   name='DiscGolfPark Mijas', city='Mijas', country='ES')

        self.expect_representation(expected='Purificación Tomás (Oviedo, ES)',
                                   name='Purificación Tomás', city='Oviedo', country='ES')

    def expect_representation(self, expected, **fields):
        course = Course(**fields)
        self.assertEqual(str(course), expected)


class DiscModelTest(TestCase):

    def test_display_name(self):
        self.expect_display_name(expected='FD', mold='FD (Jackal, Fairway Driver)')
        self.expect_display_name(expected='Explorer', mold='Explorer')

    def expect_display_name(self, expected, mold):
        disc = Disc.objects.create(mold=mold)
        self.assertEqual(disc.display_name, expected)


class DiscInBagModelTest(TestCase):

    def test_representation(self):
        self.expect_representation(expected='2x FD',
                                   amount=2, disc_mold='FD')

        self.expect_representation(expected='Explorer',
                                   amount=1, disc_mold='Explorer')

    def expect_representation(self, expected, amount, disc_mold):
        Friend.objects.all().delete()
        friend = Friend.objects.create(username='friend')
        disc = Disc.objects.create(mold=disc_mold)
        disc_in_bag = DiscInBag.objects.create(amount=amount, disc=disc, friend=friend)
        self.assertEqual(disc_in_bag.in_the_bag, expected)
