from django.test import Client, TestCase

from dialog.models import Dialog
from diary.models import Diary
from goal.models import Goal
from passphrase.models import Passphrase
from prayer.models import Prayer
from question.models import Question
from quote.models import Quote
from users.models import User


class CoreViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="shsf")
        self.client = Client()
        self.client.force_login(self.user)

        self.p1 = Passphrase.objects.create(passphrase="TEST1")

        self.q1 = Question.objects.create(index=1, question_time="morning",
                                          content="morning test question1", active=True)
        self.q2 = Question.objects.create(index=2, question_time="morning",
                                          content="morning test question2", active=True)
        self.q3 = Question.objects.create(
            index=2, question_time="night", content="night test question2", active=True)
        self.q4 = Question.objects.create(
            index=1, question_time="night", content="night test question1", active=True)
        self.quote = Quote.objects.create(
            name="-test-name", book="-test-book", content="-test- content")

        self.diary = Diary.objects.create()
        self.dialog = Dialog.objects.create(
            diary=self.diary, question=self.q1, content="-test dialog-")

        self.morning_prayer = Prayer.objects.create(
            prayer_time="morning", content="-test morning- prayer")
        self.night_prayer = Prayer.objects.create(
            prayer_time="night", content="-test night- prayer")

        self.short_goal1 = Goal.objects.create(
            content="-test short goal- 1", period="short")
        self.mid_goal1 = Goal.objects.create(
            content="-test mid goal- 1", period="mid")
        self.long_goal1 = Goal.objects.create(
            content="-test long goal- 1", period="long")

    def test_login(self):
        get_response = Client().get("/login/")
        self.assertContains(get_response, "STAY HUNGRY STAY FOOLISH")

        fail_response = Client().post("/login/", data={
            "passphrase": "FAIL"
        })
        self.assertRedirects(fail_response, "/login/")
        success_response = Client().post("/login/", data={
            "passphrase": "TEST"
        })
        self.assertRedirects(success_response, "/login/")

    def test_home(self):
        response = self.client.get('/')
        self.assertContains(response, "-test short goal-", 1)
        self.assertContains(response, "-test mid goal-", 1)
        self.assertContains(response, "-test long goal-", 1)
        self.assertContains(response, "-test dialog-")

    def test_change_short_goals_GET(self):
        response = self.client.get('/change_goals/?period=short')
        self.assertContains(response, "-test short goal-", 1)

    def test_change_short_goals_POST(self):
        response = self.client.post('/change_goals/?period=short', data={
            "form-MAX_NUM_FORMS": 2,
            "form-MIN_NUM_FORMS": 0,
            "form-INITIAL_FORMS": 1,
            "form-TOTAL_FORMS": 2,
            "form-0-id": f"{self.short_goal1.id}",
            "form-0-content": "-test1-content",
            "form-0-completion_rate": 50,
            "form-1-id": "",
            "form-1-content": "-test2-content",
            "form-1-completion_rate": 50,
        })
        self.assertEqual(Goal.objects.get(
            pk=self.short_goal1.pk).content, "-test1-content")
        self.assertEqual(Goal.objects.get(
            pk=self.short_goal1.pk).completion_rate, 50)
        self.assertEqual(Goal.objects.latest(
            "created").content, "-test2-content")
        self.assertEqual(Goal.objects.latest("created").completion_rate, 50)
        self.assertRedirects(response, "/change_goals/?period=mid")

    def test_change_mid_goals_GET(self):
        response = self.client.get('/change_goals/?period=mid')
        self.assertContains(response, "-test mid goal-", 1)

    def test_change_mid_goals_POST(self):
        response = self.client.post('/change_goals/?period=mid', data={
            "form-MAX_NUM_FORMS": 2,
            "form-MIN_NUM_FORMS": 0,
            "form-INITIAL_FORMS": 1,
            "form-TOTAL_FORMS": 2,
            "form-0-id": f"{self.mid_goal1.id}",
            "form-0-content": "-test1-content",
            "form-0-completion_rate": 50,
            "form-1-id": "",
            "form-1-content": "-test2-content",
            "form-1-completion_rate": 50,
        })
        self.assertEqual(Goal.objects.get(
            pk=self.mid_goal1.pk).content, "-test1-content")
        self.assertEqual(Goal.objects.get(
            pk=self.mid_goal1.pk).completion_rate, 50)
        self.assertEqual(Goal.objects.latest(
            "created").content, "-test2-content")
        self.assertEqual(Goal.objects.latest("created").completion_rate, 50)
        self.assertRedirects(response, "/change_goals/?period=long")

    def test_change_long_goals_GET(self):
        response = self.client.get('/change_goals/?period=long')
        self.assertContains(response, "-test long goal-", 1)

    def test_change_long_goals_POST(self):
        response = self.client.post('/change_goals/?period=long', data={
            "form-MAX_NUM_FORMS": 2,
            "form-MIN_NUM_FORMS": 0,
            "form-INITIAL_FORMS": 1,
            "form-TOTAL_FORMS": 2,
            "form-0-id": f"{self.long_goal1.pk}",
            "form-0-content": "-test1-content",
            "form-0-completion_rate": 50,
            "form-1-id": "",
            "form-1-content": "-test2-content",
            "form-1-completion_rate": 50,
        })
        self.assertEqual(Goal.objects.get(
            pk=self.long_goal1.pk).content, "-test1-content")
        self.assertEqual(Goal.objects.get(
            pk=self.long_goal1.pk).completion_rate, 50)
        self.assertEqual(Goal.objects.latest(
            "created").content, "-test2-content")
        self.assertEqual(Goal.objects.latest("created").completion_rate, 50)
        self.assertRedirects(response, "/write_diary/")

    def test_write_diary_GET(self):
        response = self.client.get('/write_diary/')
        self.assertContains(response, "Q1. night test question1")
        self.assertContains(response, "Q2. night test question2")

    def test_write_diary_POST(self):
        dialogs_len_before_post = len(Dialog.objects.all())
        response = self.client.post('/write_diary/',
                                    data={
                                        "form-0-content": "test1-content",
                                        "form-1-content": "test2-content",
                                        "form-0-question": self.q1.pk,
                                        "form-1-question": self.q2.pk,
                                        "form-MAX_NUM_FORMS": 2,
                                        "form-MIN_NUM_FORMS": 0,
                                        "form-INITIAL_FORMS": 0,
                                        "form-TOTAL_FORMS": 2,
                                    })
        dialogs_len_after_post = len(Dialog.objects.all())
        self.assertEqual(dialogs_len_after_post, dialogs_len_before_post+2)
        prayer_time = Diary.get_writing_time()
        self.assertRedirects(response, f"/prayer/?prayer_time={prayer_time}")

    def test_prayer(self):
        morning_response = self.client.get("/prayer/?prayer_time=morning")
        self.assertContains(morning_response, "-test morning- prayer")
        night_response = self.client.get("/prayer/?prayer_time=night")
        self.assertContains(night_response, "-test night- prayer")

    def test_quote_random(self):
        response = self.client.get("/quote/")
        self.assertRedirects(response, f"/quote/{self.quote.pk}/")

    def test_quote(self):
        response = self.client.get(f"/quote/{self.quote.pk}/")
        self.assertContains(response, "-test-", 3)

    def test_quote_edit(self):
        self.client.post(f"/quote/{self.quote.pk}/edit/",
                         data={"name": "changed_test_name",
                               "book": "changed_test_book",
                               "content": "changed_test_content"})
        updated_quote = Quote.objects.latest("updated")
        self.assertEqual(updated_quote.name, "changed_test_name")
        self.assertEqual(updated_quote.book, "changed_test_book")
        self.assertEqual(updated_quote.content, "changed_test_content")

    def test_quote_add(self):
        self.client.post(f"/quote/add/",
                         data={"name": "created_test_name",
                               "book": "created_test_book",
                               "content": "created_test_content"})
        created_quote = Quote.objects.latest("created")
        self.assertEqual(created_quote.name, "created_test_name")
        self.assertEqual(created_quote.book, "created_test_book")
        self.assertEqual(created_quote.content, "created_test_content")

    def test_principles(self):
        response = self.client.get('/principles/')
        self.assertContains(response, "大原則")

    def test_zen(self):
        response = self.client.get('/zen/')
        self.assertContains(response, "禪心初心")
