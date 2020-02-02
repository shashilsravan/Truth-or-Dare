from __future__ import print_function
# --------------- Helpers that build all of the responses ----------------------
import random
import boto3
import string

userid = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 15)) 
dynamodb = boto3.resource("dynamodb")

table = dynamodb.create_table(
    TableName = userid,
    KeySchema=[
        {
            'AttributeName': 'players',
            'KeyType': 'HASH' 
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'players',
            'AttributeType': 'S'
        }

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

truths = ["What is the biggest secret that you have hidden?", "What's your most embarassing momment?", 
            "who is the most Funniest person you've ever met?", "Explain about your best friend in one word?", 
            "what's your biggest fear?", "Who is your favourite person","Do you currently have a crush on anyone?", 
            "Who do you hate, and why?", "What was the last thing you searched for on your phone?",
            "What is your worst habit", "Who is the best person in this room?", "Do you have any silly nicknames?", "How many selfies do you take a day?",
            "What is something that no one else knows about you?", "Who do you think is the Beyonce of the group?"]
            
dares = ["Give a chocolate to the next person of you","Sing a favourite song of yours","Tell a joke", "Dance for your favourite song",
        "jump 10 times", "Make a prank call to your best friend", " slap the person to your right", "Be someone's pet for next 5 minutes",
        "Take an embarrassing selfie and post it as your profile picture.", "make a fake cry", "Talk without closing your mouth",
        "Call a random number, and when someone picks up, immediately start singing the National Anthem", "Do 5 pushups", "immitate anyone one in this room",
        "do 10 situps", "act like an animal", "speak for 2 minutes, without closing your mouth", "Talk like a robot", "buy a chocolate for the person to your left"
        , "Dance for a song", "Give party to the next turn's person"]
        
def build_speechlet_response_music1(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            "type": "SSML",
            "ssml": """<speak> <audio src="soundbank://soundlibrary/magic/amzn_sfx_fairy_sparkle_chimes_01"/>"""+ output + "</speak>"

        },
        'card': {
            'type': 'Simple',
            'title':  title,
            'content':  output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
    
def build_speechlet_response_music2(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            "type": "SSML",
            # 
            "ssml": """<speak> <audio src="soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_bridge_01"/>"""+ output + "</speak>"

        },
        'card': {
            'type': 'Simple',
            'title':  title,
            'content':  output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
    
def build_speechlet_response_music3(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            "type": "SSML",
            # 
            "ssml": """<speak> <audio src="soundbank://soundlibrary/wood/moves/moves_05"/>"""+ output + "</speak>"

        },
        'card': {
            'type': 'Simple',
            'title':  title,
            'content':  output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
    
def build_speechlet_response_music4(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            "type": "SSML",
            # 
            "ssml": """<speak> <audio src="soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_tally_positive_01"/>"""+ output + "</speak>"

        },
        'card': {
            'type': 'Simple',
            'title':  title,
            'content':  output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            "type": "SSML",
            "ssml": """<speak>"""+ output + "</speak>"

        },
        'card': {
            'type': 'Simple',
            'title':  title,
            'content':  output
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

def start_game(intent, session):
    session_attributes = {}
    card_title = "Start state"
    speech_output = """
        Hey! Welcome to truth or dare game . add players by saying. add. playername
    """
    reprompt_text = """
        for example, say, add john, to add john as a player
    """
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response_music2(
        card_title, speech_output, reprompt_text, should_end_session))
    
    
def store_names(intent, session):
    table = dynamodb.Table(userid)
    card_title = "Storing names"
    names = intent['slots']['name']['value']
    srv = [i for i in names.split(" ")]
    for i in srv:
        table.put_item(Item={'players':i})
        
    return main_part()
    
    
def main_part():
    card_title = "Playing game"
    response = table.scan()
    
    lst = []
    for i in response['Items']:
        lst.append(i['players'])
        
    a = random.randrange(0, len(lst))
    player = lst[a]
    
    speech_output = """
    And it's """ + player + "'s turn now. What do you want to select,  Truth or Dare?"
    session_attributes = {'players':player}
    reprompt_text = None
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response_music3(
        card_title, speech_output, reprompt_text, should_end_session))


def truth_or_dare(intent, session):
    event = intent['slots']['event']['value']
    card_title = "truth"
    
    if event.lower() == "truth":
        abc = random.choice(truths)
        speech_output = """
    """ + abc + """ <break time="3s"/>Say Next Turn, after saying truth"""
    
        reprompt_text = abc + """
        <break time="3s"/> Say Next Turn, after saying truth
        """
    
    elif event.lower() == "dare":
        abc = random.choice(dares)
        speech_output = """
""" + abc + """Say Next Turn, after the completion of dare"""

        reprompt_text = abc + """
        Say Next Turn, after saying truth
        """

    else:
        raise ValueError("Invalid event")
        
    should_end_session = False
    
    return build_response({}, build_speechlet_response_music4(
        card_title, speech_output, reprompt_text, should_end_session))


def add_player(intent, session):
    name = intent['slots']['name']['value']
    table.put_item(Item = {'players': name})
    session_attributes = {}
    card_title = "Player"
    speech_output = """
    player has been added, after adding all players, say "Done adding players". add another player by saying add, playername
    """
    reprompt_text = None
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    

def get_help_response():
    session_attributes = {}
    card_title = "Help"
    speech_output = """
        These are some of the commands to Play Truth or Dare game
        . Say let's play to start a new game
        . Add players initially by saying all names at a time
        . Add players in the middle of the game by using keyword add player name
    """
    reprompt_text = None
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
        
def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = """
    Hey! Welcome to truth or dare game. Say let's play to start a new game.
    """
    reprompt_text = "I don't know if you heard me, welcome to Truth or dare game!. Say let's play to start a new game."
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response_music1(
        card_title, speech_output, reprompt_text, should_end_session))
        

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = """
    Thank you for playing truth or dare. Hope you liked it!
    Have a nice day! """
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    
    return build_response({}, build_speechlet_response_music2(
        card_title, speech_output, None, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific 
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass

    

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "StartGameIntent":
        return start_game(intent, session)
        
    elif intent_name == "PlayerCountIntent":
        return game_started(intent, session)
        
    elif intent_name == "AMAZON.RepeatIntent":
        return handle_repeat_request(intent, session)
        
    elif intent_name == "PlayerNamesIntent":
        return main_part()
        
    elif intent_name == "TruthDareIntent":
        return truth_or_dare(intent, session)
        
    elif intent_name == "RestartGameIntent":
        return start_game(intent, session)
        
    elif intent_name == "RestartIntent":
        return main_part()
        
    elif intent_name == "AddPlayerIntent":
        return add_player(intent, session)
        
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
        
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



def lambda_handler(event, context):

    print("Incoming request...")

    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[amzn1.ask.skill.032b2028-684d-4f00-9d69-e3182aaf36e1]"):
    #     raise ValueError("Invalid Application ID")

    if ('session' in event):
        print("event.session.application.applicationId=" +
              event['session']['application']['applicationId'])
        if event['session']['new']:
            on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
                           
    if ('request' in event):                       
        if event['request']['type'] == "LaunchRequest":
            return on_launch(event['request'], event['session'])
        elif event['request']['type'] == "IntentRequest":
            return on_intent(event['request'], event['session'])
        elif event['request']['type'] == "SessionEndedRequest":
            return on_session_ended(event['request'], event['session'])