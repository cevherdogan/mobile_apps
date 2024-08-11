import json
import base64

def lambda_handler(event, context):
    try:
        # Gelen base64 kodlanmış veriyi çözüyoruz
        if 'body' in event:
            decoded_event = base64.b64decode(event['body']).decode('utf-8')
            decoded_event_json = json.loads(decoded_event)
        else:
            # Eğer base64 kodlanmamışsa, JSON olarak parse ediyoruz
            decoded_event_json = event
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Lambda fonksiyonu başarıyla çalıştı!',
                'input': decoded_event_json
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Hata oluştu!',
                'error': str(e)
            })
        }


