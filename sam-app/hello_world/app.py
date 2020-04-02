import json
import boto3  # AWS SDK for Python(PythonでAWSのリソースを操作するライブラリ)
import requests

DYNAMO_DB = boto3.client('dynamodb')  # dynamoDBを使う
TABLE_NAME = "trial"  # 操作したいdynamoDBのテーブル名
IKO_API_ENDPOINT = "https://4k86cadch8.execute-api.ap-northeast-1.amazonaws.com/Stage/hello"


def lambda_handler(event, context):
    result = DYNAMO_DB.get_item(TableName=TABLE_NAME, Key={
        'rid': {'N': "0"}
    })['Item']

    # iko_response = requests.get(IKO_API_ENDPOINT)
    validate_result = validateRequest(event)

    print(validate_result)

    # try:
    # ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    if len(validate_result) > 0:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "invalidParam": ','.join(validate_result)
            })
        }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "id": result['sid']['S'],
            "mmse": 0,
            "mmsejv": "認知症判定値",
            "mmsecm": "認知症コメント"
        }),
    }


def validateRequest(request_body):
    """
    リクエストのボディの検証
    """
    invalid_propaties = []

    if request_body['age'] < 18 or request_body['age'] > 71:
        invalid_propaties.append('age')
    if request_body['bmi'] < 10.0 or request_body['bmi'] > 100.0:
        invalid_propaties.append('bmi')
    if request_body['sbp'] < 60 or request_body['sbp'] > 300:
        invalid_propaties.append('sbp')
    if request_body['dbp'] < 30 or request_body['dbp'] > 150:
        invalid_propaties.append('dbp')
    if request_body['tg'] < 10 or request_body['tg'] > 2000:
        invalid_propaties.append('tg')
    if request_body['gpt'] < 0 or request_body['gpt'] > 1000:
        invalid_propaties.append('gpt')
    if request_body['gt'] < 0 or request_body['gt'] > 1000:
        invalid_propaties.append('gt')
    if request_body['fbs'] < 20 or request_body['fbs'] > 600:
        invalid_propaties.append('fbs')
    if request_body['hba1c'] < 3.0 or request_body['hba1c'] > 20.0:
        invalid_propaties.append('hba1c')
    if request_body['us'] < 1 or request_body['us'] > 5:
        invalid_propaties.append('us')
    if request_body['up'] < 1 or request_body['up'] > 5:
        invalid_propaties.append('up')
    if not (request_body['smoking'] == 0 or request_body['smoking'] == 1):
        invalid_propaties.append('smoking')
    return invalid_propaties
