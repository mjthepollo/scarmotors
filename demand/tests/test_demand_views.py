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
            post_dict = {'car_number': '12가1234',
                         'day_came_in': '2023-07-05',
                         'expected_day_came_out': '2023-07-19',
                         'car_model': '12', 'abroad_type': '국산',
                         'number_of_repair_works': '0',
                         'number_of_exchange_works': '0',
                         'supporter': '417',
                         'client_name': '12',
                         'insurance_agent': '60',
                         'phone_number': '01094434440',
                         'rentcar_company_name': '에스카렌트',
                         'form-TOTAL_FORMS': '1',
                         'form-INITIAL_FORMS': '0',
                         'form-MIN_NUM_FORMS': '0',
                         'form-MAX_NUM_FORMS': '1000',
                         'form-0-charge_type': '보험',
                         'form-0-charged_company': '195',
                         'form-0-order_type': '자차',
                         'form-0-receipt_number': '12-1234',
                         'form-0-fault_ratio': '80',
                         'form-0-id': '',
                         'note': '히히 똥이다!'}
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
