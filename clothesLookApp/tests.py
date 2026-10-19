"""Authorisation tests: only the owner can edit or delete a user account or a
clothing item, and anonymous visitors are sent to the login page.

Run with:  python manage.py test
"""
from django.contrib.auth import get_user_model
from django.test import TestCase

from clothesLookApp.models import Category, Clothing

User = get_user_model()


class OwnershipTestBase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user('owner', 'owner-pass-1234')
        cls.intruder = User.objects.create_user('intruder', 'intruder-pass-1234')
        cls.category = Category.objects.create(name='Shirts')
        cls.clothing = Clothing.objects.create(
            name='Blue shirt', photo='https://example.com/blue.jpg', size='M', brand='Brand',
            link='https://example.com/blue', user=cls.owner, category=cls.category)

    def user_data(self, **overrides):
        data = {'nickName': 'renamed', 'first_name': 'Ana', 'last_name': 'Ruiz',
                'sex': 'W', 'year_birth': '1990-01-31'}
        data.update(overrides)
        return data

    def clothing_data(self, **overrides):
        data = {'name': 'Red shirt', 'photo': 'https://example.com/red.jpg', 'size': 'L',
                'brand': 'Other', 'link': 'https://example.com/red', 'category': self.category.pk}
        data.update(overrides)
        return data

    def assertRedirectsToLogin(self, response):
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].startswith('/login/'), response['Location'])


class AnonymousAccessTests(OwnershipTestBase):

    def test_anonymous_cannot_open_edit_user(self):
        self.assertRedirectsToLogin(self.client.get('/edit_user/%d' % self.owner.pk))

    def test_anonymous_cannot_edit_user(self):
        response = self.client.post('/edit_user/%d' % self.owner.pk, self.user_data())
        self.assertRedirectsToLogin(response)
        self.assertEqual(User.objects.get(pk=self.owner.pk).nickName, 'owner')

    def test_anonymous_cannot_delete_user(self):
        self.assertRedirectsToLogin(self.client.post('/delete_user/%d' % self.owner.pk))
        self.assertTrue(User.objects.filter(pk=self.owner.pk).exists())

    def test_anonymous_cannot_edit_clothing(self):
        response = self.client.post('/edit/%d' % self.clothing.pk, self.clothing_data())
        self.assertRedirectsToLogin(response)
        self.assertEqual(Clothing.objects.get(pk=self.clothing.pk).name, 'Blue shirt')

    def test_anonymous_cannot_delete_clothing(self):
        self.assertRedirectsToLogin(self.client.post('/delete/%d' % self.clothing.pk))
        self.assertTrue(Clothing.objects.filter(pk=self.clothing.pk).exists())

    def test_anonymous_is_sent_to_login_from_pages_that_need_a_user(self):
        # These views used to fail with a server error for anonymous visitors.
        for url in ('/clothing/create', '/clothing/listUser', '/looks/create',
                    '/looks/listUser', '/profile/'):
            with self.subTest(url=url):
                self.assertRedirectsToLogin(self.client.get(url))


class UserOwnershipTests(OwnershipTestBase):

    def test_other_user_cannot_open_edit_page(self):
        self.client.force_login(self.intruder)
        self.assertEqual(self.client.get('/edit_user/%d' % self.owner.pk).status_code, 403)

    def test_other_user_cannot_edit_user(self):
        self.client.force_login(self.intruder)
        response = self.client.post('/edit_user/%d' % self.owner.pk, self.user_data())
        self.assertEqual(response.status_code, 403)
        self.assertEqual(User.objects.get(pk=self.owner.pk).nickName, 'owner')

    def test_other_user_cannot_delete_user(self):
        self.client.force_login(self.intruder)
        response = self.client.post('/delete_user/%d' % self.owner.pk)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(User.objects.filter(pk=self.owner.pk).exists())

    def test_owner_can_edit_own_user(self):
        self.client.force_login(self.owner)
        response = self.client.post('/edit_user/%d' % self.owner.pk, self.user_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(pk=self.owner.pk).nickName, 'renamed')

    def test_owner_can_delete_own_user(self):
        self.client.force_login(self.owner)
        response = self.client.post('/delete_user/%d' % self.owner.pk)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(pk=self.owner.pk).exists())

    def test_missing_user_returns_404(self):
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get('/edit_user/999999').status_code, 404)


class ClothingOwnershipTests(OwnershipTestBase):

    def test_other_user_cannot_edit_clothing(self):
        self.client.force_login(self.intruder)
        response = self.client.post('/edit/%d' % self.clothing.pk, self.clothing_data())
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Clothing.objects.get(pk=self.clothing.pk).name, 'Blue shirt')

    def test_other_user_cannot_delete_clothing(self):
        self.client.force_login(self.intruder)
        response = self.client.post('/delete/%d' % self.clothing.pk)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Clothing.objects.filter(pk=self.clothing.pk).exists())

    def test_owner_can_edit_clothing(self):
        self.client.force_login(self.owner)
        response = self.client.post('/edit/%d' % self.clothing.pk, self.clothing_data())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Clothing.objects.get(pk=self.clothing.pk).name, 'Red shirt')

    def test_owner_can_delete_clothing(self):
        self.client.force_login(self.owner)
        response = self.client.post('/delete/%d' % self.clothing.pk)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Clothing.objects.filter(pk=self.clothing.pk).exists())

    def test_missing_clothing_returns_404(self):
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get('/edit/999999').status_code, 404)
