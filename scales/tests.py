from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User, Group

from .models import Assements,Person


class SignupPageTest(TestCase):

    def test_signup_page_opens(self):
        response = self.client.get("/sign_up")
        self.assertEqual(response.status_code, 200)


class LoginPageTest(TestCase):

    def test_login_page_opens(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)


class MainPageProtectionTest(TestCase):

    def test_main_redirects_if_not_logged_in(self):
        response = self.client.get("/main/")
        self.assertEqual(response.status_code, 302)


class MainPageLoggedInTest(TestCase):

    def test_logged_in_user_can_open_main(self):
        User.objects.create_user(
            username="jack",
            email="jack@test.com",
            password="StrongPass123"
        )

        self.client.login(
            username="jack",
            password="StrongPass123"
        )

        response = self.client.get("/main/")
        self.assertEqual(response.status_code, 200)


class GroupTest(TestCase):

    def test_user_added_to_patient_group(self):
        group, created = Group.objects.get_or_create(name="Patient")

        user = User.objects.create_user(
            username="ali",
            password="StrongPass123"
        )

        user.groups.add(group)

        self.assertTrue(
            user.groups.filter(name="Patient").exists()
        )


class PHQ9SubmitTest(TestCase):

    def test_logged_in_user_can_submit_phq9(self):
        User.objects.create_user(
            username="patient1",
            password="StrongPass123"
        )

        self.client.login(
            username="patient1",
            password="StrongPass123"
        )

        response = self.client.post("/phq9/", {
            "q1": "1",
            "q2": "2",
            "q3": "3",
            "q4": "0",
            "q5": "1",
            "q6": "2",
            "q7": "3",
            "q8": "0",
            "q9": "1",
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Assements.objects.count(), 1)
class SignupCreatesUserAndPersonTest(TestCase):

    def test_signup_creates_user_and_person(self):
        response = self.client.post("/sign_up", {
            "username": "newpatient",
            "email": "newpatient@test.com",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "date_of_birth": "1990-01-01",
            "gender": "male",
        })

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Person.objects.count(), 1)

        user = User.objects.get(username="newpatient")
        person = Person.objects.get(user=user)

        self.assertEqual(person.gender, "male")
        self.assertRedirects(response, "/main/")
class DoctorDashboardPermissionTest(TestCase):

    def test_patient_cannot_open_doctor_dashboard(self):
        User.objects.create_user(
            username="patient",
            password="StrongPass123"
        )

        self.client.login(
            username="patient",
            password="StrongPass123"
        )

        response = self.client.get("/docs/")

        self.assertEqual(response.status_code, 302)  
class DoctorCanOpenDashboardTest(TestCase):

    def test_doctor_can_open_dashboard(self):
        doctor = User.objects.create_user(
            username="doctor",
            password="StrongPass123"
        )

        group, created = Group.objects.get_or_create(name="Doctors")
        doctor.groups.add(group)

        self.client.login(
            username="doctor",
            password="StrongPass123"
        )

        response = self.client.get("/docs/")

        self.assertEqual(response.status_code, 200)
class DoctorSearchTest(TestCase):

    def test_doctor_search_returns_patient(self):
        patient = User.objects.create_user(
            username="jackpatient",
            password="StrongPass123"
        )

        Assements.objects.create(
            user=patient,
            score_phq9=10,
            score_gad7=8
        )

        doctor = User.objects.create_user(
            username="doctor",
            password="StrongPass123"
        )

        group, created = Group.objects.get_or_create(name="Doctors")
        doctor.groups.add(group)

        self.client.login(
            username="doctor",
            password="StrongPass123"
        )

        response = self.client.get("/docs/?search=jack")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "jackpatient")
class FullAssessmentFlowTest(TestCase):

    def test_phq9_and_gad7_save_same_assessment(self):
        User.objects.create_user(
            username="patientflow",
            password="StrongPass123"
        )

        self.client.login(
            username="patientflow",
            password="StrongPass123"
        )

        phq9_response = self.client.post("/phq9/", {
            "q1": "1",
            "q2": "1",
            "q3": "1",
            "q4": "1",
            "q5": "1",
            "q6": "1",
            "q7": "1",
            "q8": "1",
            "q9": "1",
        })

        self.assertRedirects(phq9_response, "/gad7/")

        gad7_response = self.client.post("/gad7/", {
            "q_1": "1",
            "q_2": "1",
            "q_3": "1",
            "q_4": "1",
            "q_5": "1",
            "q_6": "1",
            "q_7": "1",
        })

        self.assertEqual(gad7_response.status_code, 200)

        self.assertEqual(Assements.objects.count(), 1)

        assessment = Assements.objects.first()

        self.assertEqual(assessment.score_phq9, 9)
        self.assertEqual(assessment.score_gad7, 7)

class MusicAccessTest(TestCase):

    def test_high_score_redirects_to_music_page(self):
        User.objects.create_user(
            username="highrisk",
            password="StrongPass123"
        )

        self.client.login(
            username="highrisk",
            password="StrongPass123"
        )

        self.client.post("/phq9/", {
            "q1": "3",
            "q2": "3",
            "q3": "3",
            "q4": "3",
            "q5": "3",
            "q6": "3",
            "q7": "3",
            "q8": "3",
            "q9": "3",
        })

        response = self.client.post("/gad7/", {
            "q_1": "3",
            "q_2": "3",
            "q_3": "3",
            "q_4": "3",
            "q_5": "3",
            "q_6": "3",
            "q_7": "3",
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/music")
        
        
        
        
class WeeklyRestrictionTest(TestCase):

    def test_user_with_recent_assessment_gets_end_page(self):
        user = User.objects.create_user(
            username="weeklypatient",
            password="StrongPass123"
        )

        Assements.objects.create(
            user=user,
            score_phq9=10,
            score_gad7=8
        )

        self.client.login(
            username="weeklypatient",
            password="StrongPass123"
        )

        response = self.client.get("/main/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "THANK YOU FOR YOUR TIME")
       