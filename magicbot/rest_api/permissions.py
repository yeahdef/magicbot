from os import environ

from rest_framework import permissions


class SlackTokenPermission(permissions.BasePermission):
    """Permission based on token provided by Slack integration."""

    message = 'Slack authentication token not provided or does not match SLACK_HOOK_TOKEN.'

    def has_permission(self, request, view):
        if 'token' not in request.data:
            return False
        if request.data['token'] != environ['SLACK_HOOK_TOKEN']:
            return False
        return True
