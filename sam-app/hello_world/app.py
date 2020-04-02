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

    iko_response = requests.get(IKO_API_ENDPOINT)

    print(iko_response.json())

    # try:
    # ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    return {
        "statusCode": 200,
        "body": json.dumps({
            "id": result['sid']['S'],
            "mmse": 0,
            "mmsejv": "認知症判定値",
            "mmsecm": "認知症コメント"
        }),
    }
