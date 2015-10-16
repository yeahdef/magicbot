from os import environ
import urllib

from rest_framework.exceptions import ParseError, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView


GATHERER_URI = 'http://gatherer.wizards.com/Handlers/Image.ashx?type=card'
ALIASES = {
    'bob': 'Dark Confidant',
    'bear': 'Grizzly Bears',
    'bears': 'Grizzly Bears',
    'crow': 'Storm Crow'
}


class RootView(APIView):
    """
    Nothing here but me.
    """
    def get(self, request):
        return Response({'root': 'Psst, go to the /magicslack/ endpoint.'})


class SlackMagicCardView(APIView):
    """
    Slack webhook interface for returning details of magic card.
    """
    def post(self, request):
        if 'token' not in request.data:
            raise PermissionDenied
        if request.data['token'] != environ['SLACK_HOOK_TOKEN'] and request.data['token'] != environ['SLACK_SLASH_TOKEN']:
            raise PermissionDenied

        if 'text' not in request.data:
            raise ParseError

        if request.data['text'].startswith('magicbot:'):
            print request.data['text']
            card_name = request.data['text'][9:].strip(' ')
            print type(card_name)
        else:
            card_name = unicode(request.data['text'].strip(' '), 'utf-8')

        # Catch Slack's garbage /u2019 in the name of Manor Skeleton
        print card_name
        card_name = card_name.replace(u'\u2019', u'\'')
        try:
            card_name = str(card_name)
        except UnicodeDecodeError:
            card_name = 'manor skeleton'

        if card_name.lower() in ALIASES:
            card_name = ALIASES[card_name.lower()]
        card_img_uri = '{}&name={}'.format(GATHERER_URI, urllib.quote_plus(card_name))

        return Response({
            'text': card_img_uri
        })
