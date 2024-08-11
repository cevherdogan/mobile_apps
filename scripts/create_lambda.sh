#!/bin/bash

# IAM rolünü oluşturma veya var olanı kullanma
ROLE_NAME="lambda_basic_execution"
ROLE_POLICY_NAME="LambdaBasicExecution"

# Rolün mevcut olup olmadığını kontrol et
aws iam get-role --role-name $ROLE_NAME >/dev/null 2>&1

if [ $? -ne 0 ]; then
  echo "Rol bulunamadı, oluşturuluyor..."
  aws iam create-role --role-name $ROLE_NAME --assume-role-policy-document file://../iam/trust-policy.json
  
  # Politika ekleniyor
  aws iam put-role-policy --role-name $ROLE_NAME --policy-name $ROLE_POLICY_NAME --policy-document file://../iam/policy.json
else
  echo "Rol zaten mevcut, devam ediliyor..."
fi

# Lambda fonksiyonu için zip dosyası oluşturma
cd ../lambda_function
zip function.zip lambda_function.py

# Lambda fonksiyonunu oluşturma
aws lambda create-function --function-name myLambdaFunction \
--zip-file fileb://function.zip --handler lambda_function.lambda_handler \
--runtime python3.8 --role arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/$ROLE_NAME

echo "Lambda fonksiyonu başarıyla oluşturuldu ve yüklendi."


