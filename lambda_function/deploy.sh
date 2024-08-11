#!/bin/bash

black lambda_function.py
flake8 lambda_function.py

# Değişkenler
LAMBDA_FUNCTION_NAME="myLambdaFunction"
ZIP_FILE="function.zip"

# Önceki zip dosyasını sil
if [ -f "$ZIP_FILE" ]; then
    rm $ZIP_FILE || { echo "$ZIP_FILE silinemedi!"; exit 1; }
fi

# Sadece lambda_function.py dosyasını zip ile paketleme
zip $ZIP_FILE lambda_function.py || { echo "Zip dosyası oluşturulamadı!"; exit 1; }

# Lambda fonksiyonunu AWS'ye yükleme ve güncelleme
aws lambda update-function-code --function-name $LAMBDA_FUNCTION_NAME --zip-file fileb://$ZIP_FILE || { echo "AWS Lambda güncellemesi başarısız oldu!"; exit 1; }

echo "Lambda fonksiyonu güncellendi."


