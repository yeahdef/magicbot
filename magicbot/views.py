import urllib

from bs4 import BeautifulSoup
import requests

from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from aliases import CARD_ALIASES, SET_ALIASES


GATHERER_URI = 'http://gatherer.wizards.com/Handlers/Image.ashx?type=card'


class WelcomeView(APIView):
    """This welcome view lets "Deploy to Heroku" users know that their deploy was successful."""

    permission_classes = ()

    def get(self, request):
        return Response({
            'text': 'Welcome to the magicbot API. Configure your Slack outgoing webhooks to make use of it!'
        })


class MagicCardView(APIView):
    """Slack webhook interface for returning details of magic card."""

    def post(self, request):
        if 'text' not in request.data:
            raise ParseError(detail='No query text was provided.')
        command = request.data['text']
        if command[:5] != 'test:':
            raise ParseError(detail='Text query must begin with "test:".')

        # Get set name first
        set_code = ''
        if '\\\\' in command:
            csplit = command.split('\\\\')
            set_name = csplit[1].strip(' ').lower()
            set_code = SET_ALIASES.get(set_name, '')
            command = csplit[0]

        # The 9: strips magicbot from the command
        card_name = command.encode('utf-8')[5:].strip(' ')
        # try to derive the card name from a fragment
        cards_json = requests.get('http://gatherer.wizards.com/Handlers/InlineCardSearch.ashx?nameFragment=%s' % card_name).json()
        if len(cards_json['Results']) > 0:
            card_name = cards_json['Results'][0]['Name']
        # Catch Slack's garbage /u2019 in the name of Manor Skeleton
        try:
            card_name = card_name.decode('utf-8').replace(u'\u2019', u'\'')
        except Exception as e:
            print e

        # Assign aliases
        if card_name.lower() in CARD_ALIASES:
            card_name = CARD_ALIASES[card_name.lower()]

        # Get card image uri
        card_img_uri = '{}&name={}&set={}'.format(
            GATHERER_URI, urllib.quote_plus(card_name), set_code)

        # Get card price
        set_code = set_code.upper()
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.0) Gecko/20100101 Firefox/14.0.1'}

        redirected = False
        base_uri = 'http://www.mtggoldfish.com'
        query_uri = '{}/q?query_string={}&set_id={}'.format(base_uri, card_name, set_code)
        r = requests.get(query_uri, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')

        if card_name in soup.title.string.lower():
            redirected = True

        price_uri = ''
        if not redirected:
            def is_newline(iterable):
                return iterable != '\n'
            for result in soup.find_all('tr'):
                row = filter(is_newline, result.contents)
                card_parsed = filter(is_newline, row[0].contents)
                set_parsed = filter(is_newline, row[1].contents)

                if set_code:
                    if set_code == set_parsed[0]['alt']:
                        price_uri = '{}{}#paper'.format(base_uri, card_parsed[0]['href'])
                        break
                else:
                    price_uri = '{}{}#paper'.format(base_uri, card_parsed[0]['href'])
                    break

        if price_uri or redirected:
            if not redirected:
                r = requests.get(price_uri, headers=headers)
                soup = BeautifulSoup(r.text, 'html.parser')

            def is_price_field(tag):
                if tag.has_attr('class'):
                    if tag['class'][0] == 'price-box-price':
                        return True
                return False

            try:
                price = 'Current median price: ${}'.format(soup.find_all(is_price_field)[1].string)
            except:
                price = 'Current median price: ${}'.format(soup.find_all(is_price_field)[0].string)
        else:
            price = 'Current median price: ??'

        print '{} {}'.format(card_img_uri, price)
        return Response({
            'text': '{} {}'.format(card_img_uri, price)
        })
