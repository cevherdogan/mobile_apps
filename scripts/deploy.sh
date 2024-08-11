#!/bin/bash

# Değişkenler
LAMBDA_FUNCTION_NAME="myLambdaFunction"
ZIP_FILE="function.zip"
VENV_DIR=".venv"
LAMBDA_DIR="../lambda_function"

# Önceki zip dosyasını sil
if [ -f "$LAMBDA_DIR/$ZIP_FILE" ]; then
    rm "$LAMBDA_DIR/$ZIP_FILE" || { echo "$ZIP_FILE silinemedi!"; exit 1; }
fi

# Sanal ortamı oluştur ve bağımlılıkları yükle
if [ ! -d "$LAMBDA_DIR/$VENV_DIR" ]; then
    python3 -m venv "$LAMBDA_DIR/$VENV_DIR" || { echo "Sanal ortam oluşturulamadı!"; exit 1; }
fi

source "$LAMBDA_DIR/$VENV_DIR/bin/activate"
pip install -r "$LAMBDA_DIR/requirements.txt" || { echo "Bağımlılıklar yüklenemedi!"; deactivate; exit 1; }

# Bağımlılıkları ve lambda_function.py dosyasını zip ile paketleme
cd "$LAMBDA_DIR/$VENV_DIR/lib/python3.11/site-packages"
zip -r "../../../../../$ZIP_FILE" . || { echo "Bağımlılıklar zip dosyasına eklenemedi!"; deactivate; exit 1; }
cd "../../../../../"
zip -g "$LAMBDA_DIR/$ZIP_FILE" "$LAMBDA_DIR/lambda_function.py" "$LAMBDA_DIR/requirements.txt" || { echo "Lambda fonksiyon dosyaları zip dosyasına eklenemedi!"; deactivate; exit 1; }

# Sanal ortamdan çık
deactivate

# Lambda fonksiyonunu AWS'ye yükleme ve güncelleme
aws lambda update-function-code --function-name $LAMBDA_FUNCTION_NAME --zip-file fileb://"$LAMBDA_DIR/$ZIP_FILE" || { echo "AWS Lambda güncellemesi başarısız oldu!"; exit 1; }

echo "Lambda fonksiyonu ve bağımlılıklar güncellendi."

