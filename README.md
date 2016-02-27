# Magic_the_Slackening
Simple REST interface for querying MTG card images from Slack.

## Requirements
The following env variables are required in heroku:

* SECRET_KEY (django specific)
* SLACK_HOOK_TOKEN (for webhook access)

## How to setup Slack
Configure a outgoing webhook to use the trigger word "magicbot:", set the url to (your.hosted.domain/magic-cards),
 and set the Token to whatever your SLACK_HOOK_TOKEN environment variable is.
