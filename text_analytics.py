import azure.cognitiveservices.speech as speechsdk
import requests
from pprint import pprint
from typing import Dict

def capture_speech() -> str:
    speech_key, service_region = "42104a1464d04e5082d92f951dd996da", "westus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    print("Say something...")
    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    return None

def convert_to_document(text) -> {}:
    return {
        "documents": [
                {
                    "id": "1",
                    "text": text
                }
            ]
    }

def api_request(url,documents:{}) -> {}:
    text_analytics_key = "48abb36743b141abb6302ea1cbc403bf"
    headers   = {"Ocp-Apim-Subscription-Key": text_analytics_key}
    response  = requests.post(url, headers=headers, json=documents)
    languages = response.json()
    return languages

def run_text_analysis(documents:{}):
    text_analytics_base_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.1"
    sentiment_url = f"{text_analytics_base_url}/sentiment"
    keyphrases_url = f"{text_analytics_base_url}/keyPhrases"
    entities_url = f"{text_analytics_base_url}/entities"
    urls = [sentiment_url,keyphrases_url,entities_url]
    for x in urls:
        response = api_request(x,documents)
        print(x)
        pprint(response)

if __name__ == "__main__":
    text = capture_speech()
    if text is not None:
        documents = convert_to_document(text)
        run_text_analysis(documents)
    print("...Completed")
