from os import environ

from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APISimpleTestCase


GATHERER_URI = 'http://gatherer.wizards.com/Handlers/Image.ashx?type=card'
TEST_CARD = 'manor skeleton'
TEST_CARD_GATHERER_URI = 'http://gatherer.wizards.com/Handlers/Image.ashx?type=card&name=manor+skeleton&set='
SLACK_HOOK_TOKEN = environ['SLACK_HOOK_TOKEN']


class MagicCardTests(APISimpleTestCase):
    def test_permissions_for_missing_token(self):
        url = reverse('magic-cards')
        data = {
            'text': 'magicbot: {}'.format(TEST_CARD)
        }
        r = self.client.post(url, data, format='json')
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_permissions_for_incorrect_token(self):
        url = reverse('magic-cards')
        data = {
            'token': 'INVALID_TOKEN',
            'text': 'magicbot: {}'.format(TEST_CARD)
        }
        r = self.client.post(url, data, format='json')
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_for_incorrect_query(self):
        url = reverse('magic-cards')
        data = {
            'token': SLACK_HOOK_TOKEN,
            'text': 'wrong: {}'.format(TEST_CARD)
        }
        r = self.client.post(url, data, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_basic_card_query(self):
        url = reverse('magic-cards')
        data = {
            'token': SLACK_HOOK_TOKEN,
            'text': 'magicbot: {}'.format(TEST_CARD)
        }
        r = self.client.post(url, data, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['text'], TEST_CARD_GATHERER_URI)

    def test_card_query_with_set_code(self):
        url = reverse('magic-cards')
        data = {
            'token': SLACK_HOOK_TOKEN,
            'text': 'magicbot: {} \\\\ innistrad'.format(TEST_CARD)
        }
        r = self.client.post(url, data, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['text'], '{}isd'.format(TEST_CARD_GATHERER_URI))
