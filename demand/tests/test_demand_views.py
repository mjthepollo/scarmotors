from django.test import Client, TestCase

from users.models import User


class DemandViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="superuser")
        self.user.set_password("password")
        self.user.save()
        self.client = Client()
        self.client.force_login(self.user)

        def test_get_new_register(self):
            pass

        def test_post_new_register(self):
            pass

        def test_get_edit_register(self):
            pass

        def test_post_edit_register(self):
            pass

        def test_get_edit_order(self):
            pass

        def test_post_edit_order(self):
            pass

        def test_get_search_registers(self):
            pass

        def test_post_search_registers(self):
            pass
