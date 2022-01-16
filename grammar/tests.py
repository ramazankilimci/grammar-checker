from unittest.case import expectedFailure
from django.http import response
from django.test import TestCase, Client
from .services import spell_sentence, spell_sentence_with_mark


# Create your tests here.
class ViewTests(TestCase):

    # Test Index Page
    def test_index_page_accessed_successfully(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)


    
    # Test Spellings History Page
    def test_spellings_page_accessed_successfully(self):
        c = Client()
        response = c.get('/spellings')
        self.assertEqual(response.status_code, 200)

    # Test Most Common Mistakes Page
    def test_mistakes_page_accessed_successfully(self):
        c = Client()
        response = c.get('/mistakes')
        self.assertEqual(response.status_code, 200)

    # Test spell form works successfully
    def test_spell_form_works_successfully(self):
        spell_text = "Bütün insnlar eşit doğar"
        expected_correction = 'insanlar'

        c = Client()
        url = '/'
        data = {'spell_text': spell_text}
        response = c.post(url, data)
        print('Context:', response.context[0])

        self.assertContains(response, expected_correction)

# Created for Service tests
# These are helper functions in the application
class ServiceTests(TestCase):

    # Test spell_sentence() method in SERVICES module.
    def test_spell_sentence_works_successfully(self):
        orig_text = "Bütün insnlar eşit doğar"
        expected_text = 'Bütün insanlar eşit doğar'
        
        actual_text = spell_sentence(orig_text)
        print('Actual:', actual_text)
        self.assertEqual(actual_text, expected_text)
    
    # Test spell_sentence_with_mark() method in SERVICES module.
    # It is being used to HIGHLIGHT the wrong words.
    def test_spell_sentence_with_mark_works_successfully(self):
        orig_text = "Bütün insnlar eşit doğar"
        expected_first_word = 'Bütün'
        expected_first_score = 0
        
        actual_text = spell_sentence_with_mark(orig_text)
        print('Actual:', actual_text[0][0])
        self.assertEqual(actual_text[0][0], expected_first_word)
        self.assertEqual(actual_text[0][1], expected_first_score)
        