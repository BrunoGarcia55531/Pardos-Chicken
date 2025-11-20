import json
from decimal import Decimal

from common.db import orders_table


def decimal_to_native(obj):
    
    if isinstance(obj, list):
        return [decimal_to_native(v) for v in obj]
    if isinstance(obj, dict):
        return {k: decimal_to_native(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        # si es entero, devolvemos int; si no, float
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj


def handler(event, context):
    path_params = event.get("pathParameters") or {}
    tenant_id = path_params.get("tenantId")
    order_id = path_params.get("orderId")

    if not tenant_id or not order_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "tenantId and orderId required"}),
        }

    resp = orders_table().get_item(
        Key={"tenant_id": tenant_id, "order_id": order_id}
    )

    if "Item" not in resp:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Order not found"}),
        }

    item = decimal_to_native(resp["Item"])

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(item),
    }
