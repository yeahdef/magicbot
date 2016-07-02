import urllib
import requests

from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView
from aliases import CARD_ALIASES

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
        if command[:9] != 'magicbot:':
            raise ParseError(detail='Text query must begin with "magicbot:".')

        # The 9: strips magicbot from the command
        card_name = command.encode('utf-8')[9:].strip(' ')
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
            response = '{}&name={}'.format(GATHERER_URI, urllib.quote_plus(card_name))
        else:
            response = "Card not found"
        return Response({
            'text': '{}'.format(response)
        })
