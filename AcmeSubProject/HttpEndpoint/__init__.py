import logging
import time
import uuid
import json
import azure.functions as func
from typing import List

def main(request: func.HttpRequest, subtitles: func.Out[str], translationqueue: func.Out[List[str]]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    start = time.time()
    req_body = request.get_json()
    subtitle = req_body.get("subtitle")
    languages = req_body.get("languages")

    rowKey = str(uuid.uuid4())
    data = {
        "Subtitle": subtitle,
        "PartitionKey": "subtitle",
        "RowKey": rowKey
    }
    subtitles.set(json.dumps(data))

    translation_messages = []

    for language in languages:
        translation_message = {
            "rowKey": rowKey,
            "languageCode": language
        }
        translation_messages.append(translation_message)

    translationqueue.set(json.dumps(translation_messages))

    end = time.time()
    processingTime = end - start
    
    return func.HttpResponse(
            f"Processing took {str(processingTime)} seconds. Translation is: {subtitle}",
        status_code=200
    )
