import logging
import gettext

# from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk.standard import StandardSkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractRequestInterceptor, AbstractExceptionHandler)
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import AskForPermissionsConsentCard
from ask_sdk_model.services import ServiceException

from ask_sdk_model import Response
# from alexa import data

from arcgis.gis import GIS
from arcgis.geocoding import geocode
from arcgis.geometry import Geometry, Point
import requests
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

permissions = ["read::alexa:device:all:address"]

def format_output(status_code, body):
    output = ""
    if status_code != 200:
        output += f"Status code {status_code}:"
    output += body
    return output

def get_user_address(handler_input):
    # Modified code from https://github.com/alexa/alexa-skills-kit-sdk-for-python/blob/master/samples/GetDeviceAddress/lambda/py/lambda_function.py
    # Returns status code (int) and response (str)
    status_code: int
    response: str

    req_envelope = handler_input.request_envelope
    # response_builder = handler_input.response_builder
    service_client_fact = handler_input.service_client_factory

    if not (req_envelope.context.system.user.permissions and
            req_envelope.context.system.user.permissions.consent_token):
        # response_builder.speak(("Please enable Location permissions in the Amazon Alexa app."))
        # response_builder.set_card(
        #     AskForPermissionsConsentCard(permissions=permissions))
        # return response_builder.response
        status_code = 401
        response = "Please enable Location permissions in the Amazon Alexa app."
        return status_code, response

    try:
        device_id = req_envelope.context.system.device.device_id
        device_addr_client = service_client_fact.get_device_address_service()
        addr = device_addr_client.get_full_address(device_id)

        if addr.address_line1 is None and addr.state_or_region is None:
            # response_builder.speak("It looks like you don't have an address set. You can set your address from the companion app.")
            status_code = 400
            response = "It looks like you don't have an address set. You can set your address from the companion app."
        else:
            # response_builder.speak(ADDRESS_AVAILABLE.format(
            #     addr.address_line1, addr.state_or_region, addr.postal_code))
            status_code = 200
            response = f"{addr.address_line1}, {addr.city}, {addr.state_or_region}"
        # return response_builder.response
        return status_code, response
    except ServiceException:
        # response_builder.speak("Uh Oh. Looks like something went wrong.")
        # return response_builder.response
        status_code = 500
        response = "Uh Oh. Looks like something went wrong."
        return status_code, response
    except Exception as e:
        raise e
    # user_address = "Bel-Air Drive, Ottawa, ON" # This is just a test address

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = "Welcome. I can give you infromation about the garbage day schedule."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


class GarbageDayIntentHandler(AbstractRequestHandler):
    """Handler for Garbage Day Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GarbageDayIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # _ = handler_input.attributes_manager.request_attributes["_"]
        
        # Declare return values
        speak_output = ""
        status_code = ""
        body = ""

        # Load environment variables
        API_KEY = os.environ["API_KEY"]

        # User input
        # user_address = "Bel-Air Drive, Ottawa, ON" # This is just a test address
        input_status, response = get_user_address(handler_input)
        if input_status != 200:
            speak_output = response
            return (
                handler_input.response_builder
                .speak(speak_output)
                .set_card(AskForPermissionsConsentCard(permissions=permissions))
                .response
            )
        street = response[:response.find(",")]

        # API calls
        gis = GIS(api_key=API_KEY)
        request = requests.get("https://services.arcgis.com/G6F8XLCl5KtAlZ2G/arcgis/rest/services/Solid_Waste_Collection_Calendar_Test/FeatureServer/0/query?where=1%3D1&outFields=GCD,SCHEDULE&outSR=4326&f=json")
        if request.status_code != 200:
            status_code = request.status_code
            body = "Invalid API request."
            speak_output = format_output(status_code, body)

            return (
                handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
            )

        json_dict = request.json()
        wkid = json_dict["spatialReference"]["wkid"]

        geocode_result = geocode(address=response)
        location = geocode_result[0]["location"]
        pt = Point({"x" : location["x"], "y" : location["y"], "spatialReference" : {"wkid" : wkid}})
        gcd = None
        schedule = None

        schedule_a = ["Green bin", "Garbage", "Blue bin", "Yard trimmings"]
        schedule_b = ["Black bin", "Green bin", "Yard trimmings"]

        # Search for user location in geometry
        for feature in json_dict["features"]:
            geom = Geometry(feature["geometry"])
            is_contained = geom.contains(second_geometry=pt, relation="BOUNDARY")

            if is_contained:
                gcd = feature["attributes"]["GCD"]
                schedule = feature["attributes"]["SCHEDULE"]
                break

        # Processing
        if gcd and schedule:
            status_code = 200
            body = f"The garbage collection day for {street} will be {gcd}. Make sure to take out "
            selected_schedule = schedule == 'A' and schedule_a or schedule_b
            for i in range(len(selected_schedule)):
                if i == len(selected_schedule) - 1:
                    body += "and "
                body += selected_schedule[i] + ", "
            # body += f"Garbage info for {user_address}:\n"
            # body += f"Garbage collection day: {gcd}\n"
            # body += f"Schedule: {schedule == 'A' and schedule_a or schedule_b}"
        else:
            status_code = 500
            body = "Failed to fetch garbage collection day and schedule information. Your device address might not be configured to Ottawa."

        speak_output = format_output(status_code, body)

        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = "I can tell you about the garbage day schedule. Try saying: Alexa, ottawa waste collection."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = "Goodbye."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Schedule or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        _ = handler_input.attributes_manager.request_attributes["_"]
        intent_name = ask_utils.get_intent_name(handler_input)
        # speak_output = _(data.REFLECTOR_MSG).format(intent_name)
        speak_output = "Reflected " + intent_name

        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        _ = handler_input.attributes_manager.request_attributes["_"]
        # speak_output = _(data.ERROR)
        speak_output = "An exception has occured"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


class LocalizationInterceptor(AbstractRequestInterceptor):
    """
    Add function to request attributes, that can load locale specific data
    """

    def process(self, handler_input):
        locale = handler_input.request_envelope.request.locale
        i18n = gettext.translation(
            'data', localedir='locales', languages=[locale], fallback=True)
        handler_input.attributes_manager.request_attributes["_"] = i18n.gettext

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = StandardSkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GarbageDayIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
# make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_request_handler(IntentReflectorHandler())

sb.add_global_request_interceptor(LocalizationInterceptor())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()