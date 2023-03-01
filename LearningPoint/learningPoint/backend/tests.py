from django.test import TransactionTestCase, Client
from rest_framework.test import APITestCase, APIClient, force_authenticate
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Student, Tutor, Appointment

# Test the user register case


class RegisterTestCase(APITestCase):
    # Post no data (invalid) to test if user can register or not
    def test_user_cannot_register_with_invalid_data(self):
        response = self.client.post(reverse('register'))
        self.assertEqual(response.status_code, 400)

    # Test register with valid data
    def test_user_can_register_successfully(self):
        # Define initial user data to register with
        user_data = {
            'username': 'jackjohn',
            'password': '1234@abcd',
            'email': 'landeron9999@gmail.com',
            'first_name': 'jack',
            'last_name': 'john',
            'is_staff': 1,
        }
        # Post user ata to register endpoint
        response = self.client.post(
            reverse('register'), user_data, format="json")
        self.assertEqual(response.data['email'], user_data['email'])
        self.assertEqual(response.data['username'], user_data['username'])
        self.assertEqual(response.status_code, 201)

# Test the user login case


class LoginTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'username': 'jackjohn',
            'password': '1234@abcd',
            'email': 'landeron9999@gmail.com',
            'first_name': 'jack',
            'last_name': 'john',
            'is_staff': 1,
        }

    # Test if user can log in with unverified email
    def test_user_cannot_login_with_unverified_email(self):
        self.client.post(
            self.register_url, self.user_data, format="json")

        response = self.client.post(
            self.login_url, self.user_data, format="json")

        self.assertEqual(response.status_code, 401)

    # Test if user can log in after verfication
    def test_user_can_login_after_verification(self):
        response = self.client.post(
            self.register_url, self.user_data, format="json")

        email = response.data['email']
        user = User.objects.get(email=email)
        # Set is_active status to true to indicate user has verified their email
        user.is_active = True
        user.save()

        res = self.client.post(
            self.login_url, self.user_data, format="json")

        self.assertEqual(res.status_code, 200)

# Test the create appointment case


class CreateAppointmentTestCase(APITestCase):
    # Set up initial urls and data for register and create appointment
    def setUp(self):
        self.register_url = reverse('register')
        self.user_data = {
            'username': 'jackjohn',
            'password': '1234@abcd',
            'email': 'landeron9999@gmail.com',
            'first_name': 'jack',
            'last_name': 'john',
            'is_staff': 1,
        }

        self.create_appointment_url = reverse('create_appointment')

    # Test create appointment API
    def test_create_appointment(self):
        # Firstly, register user so that can login to test the API
        response = self.client.post(
            self.register_url, self.user_data, format="json")

        user_id = response.data['id']
        email = response.data['email']
        first_name = response.data['first_name']
        last_name = response.data['last_name']

        user = User.objects.get(email=email)
        user.is_active = True
        user.save()

        tutor = Tutor.objects.create(
            user=user, id=123456, first_name=first_name, last_name=last_name, email=email)

        # Define initial appointment data to create with
        appointment_data = {
            'id': '123-abc',
            'tutor': tutor.id,
            'time': '2022-11-11 11:11:11',
            'duration': 30,
            'capacity': 10,
            'vacancy': 5,
            'location': 'E09',
            'topics': 'ELEC9609',
            'creator': 'Online'
        }

        # Login under the 'tutor' role to test the API
        self.client.login(
            username=self.user_data['username'], password=self.user_data['password'])

        # Post appointment data to the endpoint
        res = self.client.post(
            self.create_appointment_url, appointment_data, format="json")

        self.assertEqual(res.status_code, 201)

        self.client.logout()

# Test view all appointments from the point of view of tutor


class ViewAllAppointmentsTestCase(APITestCase):
    # Set up initial urls and data for register, create and view all appointments
    def setUp(self):
        self.register_url = reverse('register')
        self.user_tutor_data = {
            'username': 'jackjohn',
            'password': '1234@abcd',
            'email': 'landeron9999@gmail.com',
            'first_name': 'jack',
            'last_name': 'john',
            'is_staff': 1,
        }

        self.create_appointment_url = reverse('create_appointment')
        self.view_all_appointments_url = reverse('view_appointment_list')

    # Test view all appointments API
    def test_view_all_appointments(self):
        # Firstly, register user so that can login to test the API
        response = self.client.post(
            self.register_url, self.user_tutor_data, format="json")

        user_id = response.data['id']
        email = response.data['email']
        first_name = response.data['first_name']
        last_name = response.data['last_name']

        user = User.objects.get(email=email)
        user.is_active = True
        user.save()

        tutor = Tutor.objects.create(
            user=user, id=123456, first_name=first_name, last_name=last_name, email=email)

        # Define initial appointment data to create with
        appointment_data = {
            'id': '123-abc',
            'tutor': tutor.id,
            'time': '2022-11-11 11:11:11',
            'duration': 30,
            'capacity': 10,
            'vacancy': 5,
            'location': 'E09',
            'topics': 'ELEC9609',
            'creator': 'Online'

        }

        # Login under the 'tutor' role to test the API
        self.client.login(
            username=self.user_tutor_data['username'], password=self.user_tutor_data['password'])

        # Post appointment data to the endpoint to create an appointment
        self.client.post(
            self.create_appointment_url, appointment_data, format="json")

        # Get the list of appointments and test if the recently created appointment is there
        res = self.client.get(
            self.view_all_appointments_url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['id'], '123-abc')

        self.client.logout()

# Test book appointment from the point of view of student


class BookAppointmentTestCase(APITestCase):
    # Set up initial urls and data for register student, tutor, create appointment
    def setUp(self):
        self.register_url = reverse('register')
        self.user_tutor_data = {
            'username': 'jackjohn',
            'password': '1234@abcd',
            'email': 'landeron9999@gmail.com',
            'first_name': 'jack',
            'last_name': 'john',
            'is_staff': 1,
        }

        self.user_student_data = {
            'username': 'jackjohn1',
            'password': '1234@abcd',
            'email': 'landeron6666@gmail.com',
            'first_name': 'jack1',
            'last_name': 'john1',
            'is_staff': 0,
        }

        self.create_appointment_url = reverse('create_appointment')

    # Test book appointment API
    def test_book_appointment(self):
        # Firstly, register user tutor and student so that can login to create appointment under the 'tutor' role, and book appointment under the 'student' role
        response = self.client.post(
            self.register_url, self.user_tutor_data, format="json")

        user_id = response.data['id']
        email = response.data['email']
        first_name = response.data['first_name']
        last_name = response.data['last_name']

        user = User.objects.get(email=email)
        user.is_active = True
        user.save()

        tutor = Tutor.objects.create(
            user=user, id=123456, first_name=first_name, last_name=last_name, email=email)

        response_s = self.client.post(
            self.register_url, self.user_student_data, format="json")

        user_id_s = response_s.data['id']
        email_s = response_s.data['email']
        first_name_s = response_s.data['first_name']
        last_name_s = response_s.data['last_name']

        user_s = User.objects.get(email=email_s)
        user_s.is_active = True
        user_s.save()

        student = Student.objects.create(
            user=user_s, id=123456, first_name=first_name_s, last_name=last_name_s, email=email_s)

        # Define initial appointment data to create with
        appointment_data = {
            'id': '123-abc',
            'tutor': tutor.id,
            'time': '2022-11-11 11:11:11',
            'duration': 30,
            'capacity': 10,
            'vacancy': 5,
            'location': 'E09',
            'topics': 'ELEC9609',
            'creator': 'Online'

        }

        # Login under  the 'tutor' role to create appointment
        self.client.login(
            username=self.user_tutor_data['username'], password=self.user_tutor_data['password'])

        self.client.post(
            self.create_appointment_url, appointment_data, format="json")

        self.client.logout()

        # Login under the 'student' role to book appointment
        self.client.login(
            username=self.user_student_data['username'], password=self.user_student_data['password'])

        res = self.client.put(reverse('book_appointment', kwargs={
                              'id': appointment_data['id']}))

        # Test if the booked appointment contains the student to indicate they have booked successfully
        self.assertEqual(res.status_code, 201)
        self.assertEqual(len(res.data['students']), 1)

        self.client.logout()

# Test view booked appointments from the point of view of student


class ViewBookedAppointmentsTestCase(APITestCase):
    # Set up initial urls and data for register student, tutor, create appointment, view booked appointments
    def setUp(self):
        self.register_url = reverse('register')
        self.user_tutor_data = {
            'username': 'jackjohn',
            'password': '1234@abcd',
            'email': 'landeron9999@gmail.com',
            'first_name': 'jack',
            'last_name': 'john',
            'is_staff': 1,
        }

        self.user_student_data = {
            'username': 'jackjohn1',
            'password': '1234@abcd',
            'email': 'landeron6666@gmail.com',
            'first_name': 'jack1',
            'last_name': 'john1',
            'is_staff': 0,
        }

        self.create_appointment_url = reverse('create_appointment')
        self.view_booked_appointments_url = reverse(
            'view_booked_appointment_list')
    #  Test view booked appointments API

    def test_view_booked_appointments(self):
        # Firstly, register user tutor and student so that can login to create appointment under the 'tutor' role, and book appointment, view booked appointments under the 'student' role
        response = self.client.post(
            self.register_url, self.user_tutor_data, format="json")

        user_id = response.data['id']
        email = response.data['email']
        first_name = response.data['first_name']
        last_name = response.data['last_name']

        user = User.objects.get(email=email)
        user.is_active = True
        user.save()

        tutor = Tutor.objects.create(
            user=user, id=123456, first_name=first_name, last_name=last_name, email=email)

        response_s = self.client.post(
            self.register_url, self.user_student_data, format="json")

        user_id_s = response_s.data['id']
        email_s = response_s.data['email']
        first_name_s = response_s.data['first_name']
        last_name_s = response_s.data['last_name']

        user_s = User.objects.get(email=email_s)
        user_s.is_active = True
        user_s.save()

        student = Student.objects.create(
            user=user_s, id=123456, first_name=first_name_s, last_name=last_name_s, email=email_s)

        # Define initial appointment data to create with
        appointment_data = {
            'id': '123-abc',
            'tutor': tutor.id,
            'time': '2022-11-11 11:11:11',
            'duration': 30,
            'capacity': 10,
            'vacancy': 5,
            'location': 'E09',
            'topics': 'ELEC9609',
            'creator': 'Online'

        }

        # Login under  the 'tutor' role to create appointment
        self.client.login(
            username=self.user_tutor_data['username'], password=self.user_tutor_data['password'])

        self.client.post(
            self.create_appointment_url, appointment_data, format="json")

        self.client.logout()

        # Login under the 'student' role to book appointment, view booked appointments
        self.client.login(
            username=self.user_student_data['username'], password=self.user_student_data['password'])

        self.client.put(reverse('book_appointment', kwargs={
            'id': appointment_data['id']}))

        res = self.client.get(
            self.view_booked_appointments_url)

        # Test to see if the booked appointments list contains the recently booked appointment of student
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['id'], '123-abc')

        self.client.logout()

# Test unbook appointment from the point of view of student


class UnbookAppointmentTestCase(APITestCase):
    # Set up initial urls and data for register student, tutor, create appointment, book appointment, unbook appointment
    def setUp(self):
        self.register_url = reverse('register')
        self.user_tutor_data = {
            'username': 'jackjohn',
            'password': '1234@abcd',
            'email': 'landeron9999@gmail.com',
            'first_name': 'jack',
            'last_name': 'john',
            'is_staff': 1,
        }

        self.user_student_data = {
            'username': 'jackjohn1',
            'password': '1234@abcd',
            'email': 'landeron6666@gmail.com',
            'first_name': 'jack1',
            'last_name': 'john1',
            'is_staff': 0,
        }

        self.create_appointment_url = reverse('create_appointment')

    # Test unbook appointment API
    def test_unbook_appointment(self):
        # Firstly, register user tutor and student so that can login to create appointment under the 'tutor' role, and book appointment, unbook appointment under the 'student' role
        response = self.client.post(
            self.register_url, self.user_tutor_data, format="json")

        user_id = response.data['id']
        email = response.data['email']
        first_name = response.data['first_name']
        last_name = response.data['last_name']

        user = User.objects.get(email=email)
        user.is_active = True
        user.save()

        tutor = Tutor.objects.create(
            user=user, id=123456, first_name=first_name, last_name=last_name, email=email)

        response_s = self.client.post(
            self.register_url, self.user_student_data, format="json")

        user_id_s = response_s.data['id']
        email_s = response_s.data['email']
        first_name_s = response_s.data['first_name']
        last_name_s = response_s.data['last_name']

        user_s = User.objects.get(email=email_s)
        user_s.is_active = True
        user_s.save()

        student = Student.objects.create(
            user=user_s, id=123456, first_name=first_name_s, last_name=last_name_s, email=email_s)

        # Definie intial appointment data to create with
        appointment_data = {
            'id': '123-abc',
            'tutor': tutor.id,
            'time': '2022-11-11 11:11:11',
            'duration': 30,
            'capacity': 10,
            'vacancy': 5,
            'location': 'E09',
            'topics': 'ELEC9609',
            'creator': 'Online'

        }

        # Login under the 'tutor' role to create appointment
        self.client.login(
            username=self.user_tutor_data['username'], password=self.user_tutor_data['password'])

        self.client.post(
            self.create_appointment_url, appointment_data, format="json")

        self.client.logout()

        # Login under the 'student' role to book, unbook appointment
        self.client.login(
            username=self.user_student_data['username'], password=self.user_student_data['password'])

        res = self.client.put(reverse('book_appointment', kwargs={
                              'id': appointment_data['id']}))

        self.assertEqual(res.status_code, 201)
        self.assertEqual(len(res.data['students']), 1)

        res_u = self.client.put(reverse('unbook_appointment', kwargs={
            'id': appointment_data['id']}))

        # Test to see if the appointment is removed from the booked appointments list
        self.assertEqual(res_u.status_code, 201)
        self.assertEqual(len(res_u.data['students']), 0)

        self.client.logout()

# Test update appointment from the point of view of tutor


class UpdateAppointmentTestCase(APITestCase):
    # Set up initial urls and data for register tutor, create appointment, update appointment
    def setUp(self):
        self.register_url = reverse('register')
        self.user_tutor_data = {
            'username': 'jackjohn',
            'password': '1234@abcd',
            'email': 'landeron9999@gmail.com',
            'first_name': 'jack',
            'last_name': 'john',
            'is_staff': 1,
        }

        self.create_appointment_url = reverse('create_appointment')

    # Test update appointment API
    def test_update_appointment(self):
        # Firstly, register user tutor so that can login to create and update appointment under the 'tutor' role
        response = self.client.post(
            self.register_url, self.user_tutor_data, format="json")

        user_id = response.data['id']
        email = response.data['email']
        first_name = response.data['first_name']
        last_name = response.data['last_name']

        user = User.objects.get(email=email)
        user.is_active = True
        user.save()

        tutor = Tutor.objects.create(
            user=user, id=123456, first_name=first_name, last_name=last_name, email=email)

        # Define initial appointment data to create with
        appointment_data = {
            'id': '123-abc',
            'tutor': tutor.id,
            'time': '2022-11-11 11:11:11',
            'duration': 30,
            'capacity': 10,
            'vacancy': 5,
            'location': 'E09',
            'topics': 'ELEC9609',
            'creator': 'Online'

        }

        # Login under the 'tutor' role to create and update appointment
        self.client.login(
            username=self.user_tutor_data['username'], password=self.user_tutor_data['password'])

        res = self.client.post(
            self.create_appointment_url, appointment_data, format="json")

        self.assertEqual(res.data['location'], 'E09')
        self.assertEqual(res.data['creator'], 'Online')

        # Update some of the data of the created appointment
        appointment_data_updated = {
            'tutor': tutor.id,
            'time': '2022-11-11 11:11:11',
            'duration': 30,
            'capacity': 10,
            'vacancy': 5,
            'location': 'L10',
            'topics': 'ELEC9609',
            'creator': 'Face-to-face'
        }

        res_u = self.client.put(
            reverse('update_appointment', kwargs={
                'id': appointment_data['id']}), appointment_data_updated, format="json")

        # Test to see if the appointment contains data that hase been updated
        self.assertEqual(res_u.status_code, 201)
        self.assertEqual(res_u.data['location'], 'L10')
        self.assertEqual(res_u.data['creator'], 'Face-to-face')

        self.client.logout()

# Test delete appointment from the point of view of tutor


class DeleteAppointmentTestCase(APITestCase):
    # Set up initial urls and data for register tutor, create appointment, delete appointment
    def setUp(self):
        self.register_url = reverse('register')
        self.user_tutor_data = {
            'username': 'jackjohn',
            'password': '1234@abcd',
            'email': 'landeron9999@gmail.com',
            'first_name': 'jack',
            'last_name': 'john',
            'is_staff': 1,
        }

        self.create_appointment_url = reverse('create_appointment')
        self.view_all_appointments_url = reverse('view_appointment_list')

    # Test delete appointment API
    def test_delete_appointment(self):
        # Firstly, register user tutor so that can login to create and delete appointment under the 'tutor' role
        response = self.client.post(
            self.register_url, self.user_tutor_data, format="json")

        user_id = response.data['id']
        email = response.data['email']
        first_name = response.data['first_name']
        last_name = response.data['last_name']

        user = User.objects.get(email=email)
        user.is_active = True
        user.save()

        tutor = Tutor.objects.create(
            user=user, id=123456, first_name=first_name, last_name=last_name, email=email)

        # Define intial appointment data to create with
        appointment_data = {
            'id': '123-abc',
            'tutor': tutor.id,
            'time': '2022-11-11 11:11:11',
            'duration': 30,
            'capacity': 10,
            'vacancy': 5,
            'location': 'E09',
            'topics': 'ELEC9609',
            'creator': 'Online'

        }

        # Login under the 'tutor' to create, view appointments
        self.client.login(
            username=self.user_tutor_data['username'], password=self.user_tutor_data['password'])

        self.client.post(
            self.create_appointment_url, appointment_data, format="json")

        res = self.client.get(
            self.view_all_appointments_url)

        # Test to see if the all appointments list contains the recently created appointment
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['id'], '123-abc')

        # Test to see if the API returns successful response status
        res_d = self.client.delete(
            reverse('delete_appointment', kwargs={
                'id': appointment_data['id']}))

        self.assertEqual(res_d.status_code, 200)

        # Test to see if the appointment has been removed from the list
        res_v = self.client.get(
            self.view_all_appointments_url)

        self.assertEqual(res_v.status_code, 200)
        self.assertEqual(len(res_v.data), 0)

        self.client.logout()

# Test the change password case


class ChangePasswordTestCase(APITestCase):
    # Set up initial urls and data for register user, change password
    def setUp(self):
        self.register_url = reverse('register')
        self.user_data = {
            'username': 'jackjohn',
            'password': '1234@abcd',
            'email': 'landeron9999@gmail.com',
            'first_name': 'jack',
            'last_name': 'john',
            'is_staff': 1,
        }

        self.change_password_url = reverse('change_password')

    # Test change password API
    def test_change_password(self):
        # Firstly, register user so that can login to test the API
        response = self.client.post(
            self.register_url, self.user_data, format="json")

        user_id = response.data['id']
        email = response.data['email']
        first_name = response.data['first_name']
        last_name = response.data['last_name']

        user = User.objects.get(email=email)
        user.is_active = True
        user.save()

        # Define data with old and new passwords to post to the endpoint
        data = {'old_password': '1234@abcd', 'new_password': '12345@abcde'}

        # Login to test the API
        self.client.login(
            username=self.user_data['username'], password=self.user_data['password'])

        res = self.client.put(
            self.change_password_url, data, format="json")

        # Test to see if it returns successul response status
        self.assertEqual(res.status_code, 200)

        self.client.logout()

# Test the reset password case


class ResetPasswordTestCase(APITestCase):
    # Set up initial urls and data for register user, reset password
    def setUp(self):
        self.register_url = reverse('register')
        self.user_data = {
            'username': 'jackjohn',
            'password': '1234@abcd',
            'email': 'landeron9999@gmail.com',
            'first_name': 'jack',
            'last_name': 'john',
            'is_staff': 1,
        }

        self.reset_password_url = reverse('reset_password')

    # Test reset password API
    def test_reset_password(self):
        # Firstly, register user so that can login to test the API
        response = self.client.post(
            self.register_url, self.user_data, format="json")

        user_id = response.data['id']
        email = response.data['email']
        first_name = response.data['first_name']
        last_name = response.data['last_name']

        user = User.objects.get(email=email)
        user.is_active = True
        user.save()

        # Define data with email to post to the endpoint
        data = {'email': 'landeron9999@gmail.com'}

        # Login to test the API
        self.client.login(
            username=self.user_data['username'], password=self.user_data['password'])

        res = self.client.post(
            self.reset_password_url, data, format="json")

        # Test to see if it returns successul response status
        self.assertEqual(res.status_code, 200)

        self.client.logout()

# Test the view profile case


class ViewProfileTestCase(APITestCase):
    # Set up initial urls and data for register user, view profile
    def setUp(self):
        self.register_url = reverse('register')
        self.user_data = {
            'username': 'jackjohn',
            'password': '1234@abcd',
            'email': 'landeron9999@gmail.com',
            'first_name': 'jack',
            'last_name': 'john',
            'is_staff': 1,
        }

        self.view_profile_url = reverse('profile')

    # Test view profile API
    def test_view_profile(self):
        # Firstly, register user so that can login to test the API
        response = self.client.post(
            self.register_url, self.user_data, format="json")

        user_id = response.data['id']
        email = response.data['email']
        first_name = response.data['first_name']
        last_name = response.data['last_name']

        user = User.objects.get(email=email)
        user.is_active = True
        user.save()

        tutor = Tutor.objects.create(
            user=user, id=123456, first_name=first_name, last_name=last_name, email=email)

        # Login to test the API
        self.client.login(
            username=self.user_data['username'], password=self.user_data['password'])

        res = self.client.get(
            self.view_profile_url)

        # Test to see if it returns successul response status
        self.assertEqual(res.status_code, 200)

        # Test to see if the reponse contains the data created
        self.assertEqual(res.data['first_name'], 'jack')
        self.assertEqual(res.data['last_name'], 'john')
        self.assertEqual(res.data['email'], 'landeron9999@gmail.com')

        self.client.logout()


class UpdateProfileTestCase(APITestCase):
    # Set up initial urls and data for register user, update profile
    def setUp(self):
        self.register_url = reverse('register')
        self.user_data = {
            'username': 'jackjohn',
            'password': '1234@abcd',
            'email': 'landeron9999@gmail.com',
            'first_name': 'jack',
            'last_name': 'john',
            'is_staff': 1,
        }

        self.view_profile_url = reverse('profile')

    # Test update profile API
    def test_update_profile(self):
        # Firstly, register user so that can login to test the API
        response = self.client.post(
            self.register_url, self.user_data, format="json")

        user_id = response.data['id']
        email = response.data['email']
        first_name = response.data['first_name']
        last_name = response.data['last_name']

        user = User.objects.get(email=email)
        user.is_active = True
        user.save()

        tutor = Tutor.objects.create(
            user=user, id=123456, first_name=first_name, last_name=last_name, email=email)

        # Define data for updated profile
        profile_updated = {
            'first_name': 'ron',
            'last_name': 'roy',
            'email': 'landeron6666@gmail.com'
        }

        # Login to test the API
        self.client.login(
            username=self.user_data['username'], password=self.user_data['password'])

        res = self.client.get(
            self.view_profile_url)

        # Test to see if it returns successul response status
        self.assertEqual(res.status_code, 200)

        # Test to see if the reponse contains the data created
        self.assertEqual(res.data['first_name'], 'jack')
        self.assertEqual(res.data['last_name'], 'john')
        self.assertEqual(res.data['email'], 'landeron9999@gmail.com')

        res_u = self.client.put(reverse('update_profile', kwargs={
            'id': user_id}), profile_updated, format="json")

        # Test to see if it returns successul response status
        self.assertEqual(res_u.status_code, 201)

        # Test to see if the reponse contains the data updated
        self.assertEqual(res_u.data['first_name'], 'ron')
        self.assertEqual(res_u.data['last_name'], 'roy')
        self.assertEqual(res_u.data['email'], 'landeron6666@gmail.com')

        self.client.logout()
