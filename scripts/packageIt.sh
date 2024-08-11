#!/bin/bash

# Tek bir dosyada tüm işlemleri içeren Lambda fonksiyonunu zip ile paketleme
# cd ../lambda_function
zip -r function.zip ../lambda_function/lambda_function.py ../lambda_function/__init__.py
# cd ..

# Lambda fonksiyonunu AWS'ye yükleme ve güncelleme
aws lambda update-function-code --function-name myLambdaFunction --zip-file fileb://../lambda_function/function.zip

# Bellek ve timeout ayarlarını güncelleme
aws lambda update-function-configuration --function-name myLambdaFunction --timeout 10 --memory-size 256

echo "Lambda fonksiyonu başarıyla güncellendi."


