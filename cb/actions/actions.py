# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
import google.generativeai as genai

# Replace with your actual Google AI API key
api_key = "AIzaSyBT8sTiySSb7b1rqVDgNhyD9BGz51hyOY8"  # Ensure to use a valid API key

# Configure the Generative AI API
genai.configure(api_key=api_key)

# Generation configuration
generation_config = {
    "temperature": 1.0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

class ActionCallGeminiAPI(Action):
    def name(self) -> Text:
        return "action_call_gemini_api"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the latest message sent by the user
        user_message = tracker.latest_message['text']


        try:
            # Start a new chat session
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
            )
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(user_message)

            # Get the generated response
            generated_response = response.text

            # Send the response back to the user
            dispatcher.utter_message(text=generated_response)

        except Exception as e:
            dispatcher.utter_message(text="Sorry, I couldn't fetch details from the API at the moment.")

        return []