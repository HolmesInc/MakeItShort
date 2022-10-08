from django.test import TestCase
from django.urls import reverse
from .models import User, UserLink, URL


class LinkTransformerIndexViewTests(TestCase):
    def test_index(self):
        """
        Test best case for link_transformer index view
        """
        response = self.client.get(reverse('link_transformer:index'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ['link_transformer/index.html'])


class LinkTransformerShortURLViewTests(TestCase):
    def test_short_url_invalid_url(self):
        """
        Test fail response from link_transformer short url view
        """
        response = self.client.post(reverse('link_transformer:short_url'), {'input_url': '123'})

        self.assertEqual(response.status_code, 400)

    def test_short_url_with_data_creation(self):
        """
        Test successful response from link_transformer short url view
        """
        expected_base_url = 'http://testserver/'
        response = self.client.post(reverse('link_transformer:short_url'), {'input_url': 'https://www.google.com/'})

        self.assertEqual(response.status_code, 200)
        self.assertIn(expected_base_url, response.context['short_url'])
        self.assertEqual(response.context['link_clicks'], 0)
        self.assertEqual(len(response.context['short_url'].replace(expected_base_url, '')), 10)

    def test_short_url_db_data_with_data_creation(self):
        """
        Test DB data after successful execution of link_transformer short url view
        """
        expected_base_url = 'http://testserver/'
        response = self.client.post(reverse('link_transformer:short_url'), {'input_url': 'https://www.google.com/'})

        print()
