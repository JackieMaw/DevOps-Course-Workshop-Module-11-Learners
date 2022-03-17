import logging
import json
import uuid

import azure.functions as func

def main(msg: func.QueueMessage, subtitlestablein: str, subtitlestableout: func.Out[str]) -> None:

    message_body_text = msg.get_body().decode('utf-8')
    logging.info('Python queue trigger function processed a queue item: %s', message_body_text)

    subtitle_table_row_in = json.loads(subtitlestablein)
    logging.info('Retrieved table row from subtitlestablein: %s', subtitle_table_row_in)

    message_body = json.loads(message_body_text)
    languageCode = message_body["languageCode"]
    
    subtitle = subtitle_table_row_in["Subtitle"]
    rowKey = str(uuid.uuid4())
    subtitle_table_row_out = {
        "Subtitle": subtitle.upper(),
        "Language": languageCode,
        "PartitionKey": "subtitle",
        "RowKey": rowKey
    }
    subtitlestableout.set(json.dumps(subtitle_table_row_out))
    logging.info('Saved table row to subtitlestableout: %s', subtitle_table_row_out)
