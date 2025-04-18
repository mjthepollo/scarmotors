import pytest
from django.test import Client, TestCase

from users.models import User


@pytest.mark.view_test
class CoreViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="superuser")
        self.user.set_password("password")
        self.user.save()
        self.client = Client()
        self.client.force_login(self.user)

    def test_login(self):
        self.client.logout()
        fail_response = Client().post("/login/", data={
            "username": "failuser",
            "password": "password",
        })
        self.assertContains(fail_response, "올바른 사용자 이름와/과 비밀번호를 입력하십시오. ")
        success_response = Client().post("/login/", data={
            "username": "superuser",
            "password": "password",
        })
        self.assertRedirects(success_response, "/")
