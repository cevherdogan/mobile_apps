base64 -i ../lambda_function/test_event.json -o encoded_payload.txt
aws lambda invoke --function-name myLambdaFunction --payload fileb://encoded_payload.txt response.json

cat response.json | jq -r '.body | fromjson'

