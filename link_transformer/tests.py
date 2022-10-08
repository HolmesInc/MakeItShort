from django.test import TestCase
from django.urls import reverse
from .models import User, UserLink, URL, LinkClick


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
        input_url = 'https://www.google.com/'
        expected_base_url = 'http://testserver/'

        # validate DB tables are empty before test execution
        self.assertEqual(len(User.objects.all()), 0)
        self.assertEqual(len(UserLink.objects.all()), 0)
        self.assertEqual(len(URL.objects.all()), 0)
        self.assertEqual(len(LinkClick.objects.all()), 0)

        self.client.post(reverse('link_transformer:short_url'), {'input_url': input_url})

        # validate users created
        users = User.objects.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].user_hash, 'a589d1f8fbfa428d037a55bd5d5373a834efc4591ac40dd96558c91f')

        # validate urls created
        urls = URL.objects.all()
        self.assertEqual(len(urls), 1)
        self.assertEqual(urls[0].origin_url, input_url)

        # validate user links created
        user_links = UserLink.objects.all()
        self.assertEqual(len(user_links), 1)
        self.assertEqual(UserLink.objects.all()[0].url_id, urls[0])
        self.assertEqual(UserLink.objects.all()[0].user_id, users[0])
        self.assertIn(expected_base_url, user_links[0].short_url)

        # validate counter
        link_clicks = LinkClick.objects.all()
        self.assertEqual(len(link_clicks), 0)


class LinkTransformerShortLinkDispatcherViewTests(TestCase):
    def test_short_url_invalid_url_hash(self):
        """
        Test fail response from link_transformer short url dispatcher view with invalid usl hash
        """
        response = self.client.get(reverse('link_transformer:short_url_dispatcher', args=[123]))

        self.assertEqual(response.status_code, 404)

    def test_short_url_no_user_link(self):
        """
        Test fail response from link_transformer short url dispatcher view with no user links created
        """
        response = self.client.get(reverse('link_transformer:short_url_dispatcher', args=['123qwe33d1']))

        self.assertEqual(response.status_code, 404)

    def test_short_url_successful_dispatch(self):
        """
        Test success response from link_transformer short url dispatcher view
        """
        user_hash = 'a589d1f8fbfa428d037a55bd5d5373a834efc4591ac40dd96558c91f'
        user = User(user_hash=user_hash)
        user.save()
        url = URL(origin_url='input_url.com')
        url.save()
        url_hash = '123qwe33d1'
        UserLink(url_id=url, user_id=user, short_url=f'short_url.com/{url_hash}', url_hash=url_hash).save()
        response = self.client.get(reverse('link_transformer:short_url_dispatcher', args=[url_hash]))

        self.assertEqual(response.status_code, 302)
        link_clicks = LinkClick.objects.all()
        self.assertEqual(len(link_clicks), 1)
