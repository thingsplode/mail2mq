pip install awscli --upgrade
pip install --user --upgrade aws-sam-cli
pip install stomp.py

### Create and activate a virtual environment

```bash
python3 -m venv ./venv
source ./venv/bin/activate
pip install stomp.py
```
### Build & deploy the function using aws cli

```bash
pushd venv/lib/python3.7/site-packages && \
zip -r9 ../../../../mailfunc.zip . \
popd
zip -g mailfunc.zip receiver.py
```

### Create the function

```bash
aws lambda create-function --function-name mail2mq \
--zip-file fileb://mailfunc.zip \
--handler receiver.handle_mail --runtime python3.7 \
--role "arn:aws:iam::307733074768:role/cognitoa14ae85b_userpoolclient_lambda_role" \
--environment Variables="{MQHOST=b-77b1a0da-2ad5-4823-a5c5-17e10dab3e8d-1.mq.eu-west-1.amazonaws.com,MQPORT=61614}"
```

### Invoke the function
```bash
aws lambda invoke --function-name mail2mq --payload "$(cat rcvd_email.json)" output.txt
```
You can check the execution output by issuing the following command:
```bash
cat ouput.txt |jq .
```

### Update the function after code change

```bash
zip -g mailfunc.zip receiver.py
aws lambda update-function-code --function-name mail2mq --zip-file fileb://mailfunc.zip
```