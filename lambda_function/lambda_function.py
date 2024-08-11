import json
import base64
import os

def lambda_handler(event, context):
    enable_logging = os.getenv('ENABLE_LOGGING', 'false').lower() == 'true'

    def log(message):
        if enable_logging:
            print(message)

    try:
        if 'body' in event:
            decoded_event = base64.b64decode(event['body']).decode('utf-8')
            decoded_event_json = json.loads(decoded_event)
        else:
            decoded_event_json = event

        log(f"Decoded event: {decoded_event_json}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Lambda fonksiyonu başarıyla çalıştı!',
                'input': decoded_event_json
            })
        }
    except json.JSONDecodeError as e:
        log(f"JSON decoding error: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Geçersiz JSON formatı!',
                'error': str(e)
            })
        }
    except base64.binascii.Error as e:
        log(f"Base64 decoding error: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Geçersiz base64 verisi!',
                'error': str(e)
            })
        }
    except Exception as e:
        log(f"Unhandled error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Bilinmeyen bir hata oluştu!',
                'error': str(e)
            })
        }


