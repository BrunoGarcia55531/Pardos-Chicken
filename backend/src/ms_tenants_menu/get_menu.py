import json
from decimal import Decimal
from boto3.dynamodb.conditions import Key

from common.db import menu_table


def decimal_to_native(obj):
    if isinstance(obj, list):
        return [decimal_to_native(v) for v in obj]
    if isinstance(obj, dict):
        return {k: decimal_to_native(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj


def handler(event, context):
    path_params = event.get("pathParameters") or {}
    tenant_id = path_params.get("tenantId", "pardos-chicken")

    table = menu_table()
    resp = table.query(
        KeyConditionExpression=Key("tenant_id").eq(tenant_id)
    )
    items = resp.get("Items", [])

    items = decimal_to_native(items)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(items),
    }
