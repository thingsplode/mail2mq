#!/usr/bin/env bash
FUNCTION_ARCH=mailfunc.zip
FUNCTION_NAME=mail2mq
zip -g ${FUNCTION_ARCH} ./*.py
echo "updating..."
aws lambda update-function-code --function-name ${FUNCTION_NAME} --zip-file fileb://${FUNCTION_ARCH}
echo "invoking..."
aws lambda invoke --function-name ${FUNCTION_NAME} --payload "$(cat rcvd_email.json)" output.txt
echo "[Output]"
cat ./output.txt
