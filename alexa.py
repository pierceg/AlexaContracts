"""
This Alexa tool can create contracts on voice command using SpringCM's API.
"""

from __future__ import print_function
#import requests
import json


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------
def spring_auth():
    """url = "https://authuat.springcm.com/api/v201606/apiuser"

    payload = "{\n  \"client_id\": \"46039299-c12e-4903-81c7-0e5006279d8c\",\n  \"client_secret\": \"b3bccf7cc9ae4a96bac60b9d33fa67f48dAOeNoU49YM4Ykp1Ul5YZwTJAQMCRFcJ7sBgLYyZk73idHgoTCkwk1jrqFe6bRn46D7piIp6xgxc3up2uitOfpiFJUzG318\"\n}"
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "8e6438ed-62c9-9e22-856b-f35eb01ca0d1"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    response_data = json.loads(response.text)
    return response_data['access_token']"""
    return None

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Spring CM Alexa integration." \
                    "Please tell me what it is you want to do."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I can build NDAs."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the SpringCM Alexa integration."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_NDA_attributes(acct_name, acct_address, acct_city, acct_state, acct_zip, acct_country):
    return {"accountName": acct_name,
            "accountAddress": acct_address,
            "accountCity":acct_city,
            "accountState":acct_state,
            "accountZip":acct_zip,
            "accountCountry":acct_country}


def set_color_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'NDA' in intent['slots']:
        """
        favorite_color = intent['slots']['Color']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        """
        speech_output = "I'm building an NDA for you."
        reprompt_text = "I'll send it to you when I'm done." \
                        "You can send it out or edit it after I'm finished."
    else:
        speech_output = "I don't understand what you asked me to do," \
                        "please repeat that"
        reprompt_text = "If you want, I can build NDAs."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_color_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite color is " + favorite_color + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "You can say, my favorite color is red."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def build_NDA(intent, session):
    card_title = intent['name']
    session_attributes = session['attributes']
    should_end_session = False

    #confirm we have contract type
    if intent['slots']['ContractType'] and intent['slots']['ContractTarget']:
        speech_output = "I'm going to build you an NDA now"
        contractType = intent['slots']['ContractType']['value']
        contractTarget = intent['slots']['ContractTarget']['value']
        #accountId = getAccountId(contractTarget)
        accountId = "001c000001BU1pfAAD"
        #spriAccess = spring_auth()
        reprompt_text = ""

    else:
        speech_output = "Sorry, not a valid command"
        reprompt_text = "Ask me to create a contract for a specific account"


    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch

    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "CreateNDA":
        return build_NDA(intent,session)

    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest" and event['request']['intent']['slots']['ContentType']:
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
