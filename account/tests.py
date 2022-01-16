from django.test import TestCase, Client

# Create your tests here.
class ViewTests(TestCase):

    # Test Index Page
    def test_login_page_accessed_successfully(self):
        c = Client()
        response = c.get('/account/login')
        self.assertEqual(response.status_code, 301)

    # Test Logout Page
    def test_logout_page_accessed_successfully(self):
        c = Client()
        response = c.get('/account/logout')
        self.assertEqual(response.status_code, 301)

    # Test Registration Page
    def test_signup_page_accessed_successfully(self):
        c = Client()
        response = c.get('/account/register')
        self.assertEqual(response.status_code, 301)

    # Test Registration Form
    def test_signup_form_worked_successfully(self):
        c = Client()
        url = '/account/register'
        data = {'username': 'piko',
                'first_name': 'Piko',
                'last_name': 'Pike',
                'email': 'piko@piko.io',
                'password1': 'Sevgileriyarinlarabiraktiniz2022!',
                'password2': 'Sevgileriyarinlarabiraktiniz2022!'
                }
        response = c.post(url, data)
        print('context: ', response.status_code)
        print('response', response)
        self.assertEqual(response.status_code, 301)

