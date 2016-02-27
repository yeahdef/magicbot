from os import environ
import urllib

from rest_framework.exceptions import ParseError, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from aliases import CARD_ALIASES, SET_ALIASES


GATHERER_URI = 'http://gatherer.wizards.com/Handlers/Image.ashx?type=card'


class MagicCardView(APIView):
    """Slack webhook interface for returning details of magic card."""
    def post(self, request):
        print 'anything?'

        if 'token' not in request.data:
            raise PermissionDenied
        if request.data['token'] != environ['SLACK_HOOK_TOKEN']:
            raise PermissionDenied
        if 'text' not in request.data:
            raise ParseError
        command = request.data['text']

        # Get set name first
        set_code = ''
        if '\\\\' in command:
            csplit = command.split('\\\\')
            set_name = csplit[1].strip(' ').lower()
            set_code = SET_ALIASES.get(set_name, '')
            command = csplit[0]

        # The 9: strips magicbot from the command
        card_name = command.encode('utf-8')[9:].strip(' ')

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

        return Response({
            'text':  card_img_uri
        })
