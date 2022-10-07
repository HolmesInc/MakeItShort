from django.test import TestCase
from django.urls import reverse


class LinkTransformerIndexViewTests(TestCase):
    def test_index(self):
        """
        Test best case for link_transformer index view
        """
        response = self.client.get(reverse('link_transformer:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ['link_transformer/index.html'])
