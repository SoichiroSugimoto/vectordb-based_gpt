import os
import json
import boto3
import ast
import datetime
from urllib import parse
from dotenv import load_dotenv

from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

class DynamoDBTable:
    def __init__(self, table_name, region_name, partition_key_name, sort_key_name):
        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name=region_name,
        )
        self.table = self.dynamodb.Table(table_name)
        self.partition_key_name = partition_key_name
        self.sort_key_name = sort_key_name

    def put_item(self, item):
        res = self.table.put_item(Item=item)
        return res

    def get_item(self, key):
        res = self.table.get_item(Key=key)
        return res["Item"] if "Item" in res else None

    def get_items_beginning_with(self, partition_key, sort_key_prefix):
        res = self.table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key(self.partition_key_name).eq(partition_key)
            & boto3.dynamodb.conditions.Key(self.sort_key_name).begins_with(sort_key_prefix)
        )
        return res["Items"]

    
    # partition_key_prefixes(配列)から始まるパーティションキーを持つアイテムを取得
    def query_items(self, partition_key_prefixes=None, sort_key_value=0):
        results = []
        if partition_key_prefixes is not None:
            for prefix in partition_key_prefixes:
                response = self.table.query(
                    KeyConditionExpression=Key(self.partition_key_name).begins_with(prefix) & Key(self.sort_key_name).eq(sort_key_value)
                )
                results.extend(response['Items'])
        return results


    def get_alive_records(self):
        res = self.table.scan(FilterExpression=Attr("deleted").eq(0))
        return res["Items"] if "Item" in res else None

    def get_all_items(self):
        res = self.table.scan()
        return res["Items"]

    def update_item(self, key, update_expression, expression_attribute_values):
        res = self.table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW",
        )
        return res
