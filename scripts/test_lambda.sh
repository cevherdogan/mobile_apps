encoded_payload=$(base64 <<< '{"key1":"value1","key2":"value2","key3":"value3"}')
aws lambda invoke --function-name myLambdaFunction --payload "$encoded_payload" response.json

cat response.json | jq -r '.body | fromjson'




