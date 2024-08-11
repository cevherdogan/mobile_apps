#!/bin/bash

aws lambda update-function-configuration --function-name myLambdaFunction --timeout 10 --memory-size 256

echo "Lambda fonksiyonu bellek ve timeout ayarları güncellendi."


