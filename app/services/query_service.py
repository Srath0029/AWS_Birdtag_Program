# query_service.py
import boto3
import logging
from urllib.parse import urlparse
from botocore.exceptions import BotoCoreError, ClientError
from typing import Dict, List, Optional, Tuple

dynamodb = boto3.client('dynamodb')
TABLE_NAME = "BirdDetections"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def search_files_by_species_and_mincount(required_tags: dict) -> list[str]:
    """
    Query DynamoDB and return URLs of files that have at least the minimum counts
    for all specified bird species.
    """
    try:
        response = dynamodb.scan(TableName=TABLE_NAME)
        items = response.get('Items', [])
    except Exception as e:
        raise RuntimeError(f"Failed to scan table: {str(e)}")

    matching_urls = []
    for item in items:
        item_tags = item.get("tags", {}).get("M", {})
        match = True
        for tag, count in required_tags.items():
            if tag not in item_tags:
                match = False
                break
            item_count = int(item_tags[tag]["N"])
            if item_count < count:
                match = False
                break
        if match:
            file_type = item.get("file_type", {}).get("S")
            if file_type == "image":
                url = item.get("thumbnail_url", {}).get("S")
            else:
                url = item.get("file_url", {}).get("S")
            if url:
                matching_urls.append(url)
    return matching_urls

def search_by_species(tags: Dict[str, bool]) -> List[str]:
    try:
        response = dynamodb.scan(TableName=TABLE_NAME)
        items = response.get("Items", [])
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"DynamoDB scan failed: {str(e)}")

    matching_urls = []
    for item in items:
        item_tags = item.get("tags", {}).get("M", {})
        if all(tag in item_tags for tag in tags):
            file_type = item.get("file_type", {}).get("S")
            if file_type == "image":
                url = item.get("thumbnail_url", {}).get("S")
            else:
                url = item.get("file_url", {}).get("S")
            if url:
                matching_urls.append(url)

    return matching_urls

def get_original_from_thumbnail(thumbnail_url: str) -> Optional[str]:
    try:
        response = dynamodb.scan(TableName=TABLE_NAME)
        items = response.get("Items", [])
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"DynamoDB scan failed: {str(e)}")

    for item in items:
        item_thumb = item.get("thumbnail_url", {}).get("S")
        if item_thumb == thumbnail_url:
            return item.get("file_url", {}).get("S")

    return None

def extract_keys_from_url(url: str) -> Tuple[Optional[str], Optional[str]]:
    parsed_url = urlparse(url)
    key = parsed_url.path.lstrip('/')

    if key.startswith("thumbnails/"):
        source_file_name = key[len("thumbnails/"):].replace("-thumb", "")
        source_path = "uploads/" + source_file_name
    else:
        source_path = key

    try:
        response = dynamodb.query(
            TableName=TABLE_NAME,
            KeyConditionExpression="#sp = :sp",
            ExpressionAttributeNames={"#sp": "source_path"},
            ExpressionAttributeValues={":sp": {"S": source_path}}
        )
        items = response.get("Items", [])
        if not items:
            return None, None
        timestamp = items[0]["timestamp"]["S"]
        return source_path, timestamp
    except Exception as e:
        logger.error(f"Error querying DynamoDB for source_path {source_path}: {str(e)}")
        return None, None


def update_tags_for_files(urls: List[str], operation: int, tags_list: List[str]) -> int:
    # Parse tag entries into dictionary {tag_name: count}
    tags_to_update: Dict[str, int] = {}
    for tag_entry in tags_list:
        try:
            tag_name, count_str = tag_entry.split(",")
            count = int(count_str)
            if count <= 0:
                continue
            tags_to_update[tag_name] = count
        except Exception:
            # Skip malformed tags
            continue

    if not tags_to_update:
        raise ValueError("No valid tags provided.")

    updated_files = 0

    for url in urls:
        source_path, timestamp = extract_keys_from_url(url)
        if not source_path or not timestamp:
            logger.warning(f"No items found for key {url}")
            continue

        expr_attr_names = {
            "#tags": "tags",
            "#sp": "source_path",
            "#ts": "timestamp"
        }
        expr_attr_values = {":zero": {"N": "0"}}
        update_expr_parts = []

        for tag, count in tags_to_update.items():
            tag_key = f"#tag_{tag}"
            expr_attr_names[tag_key] = tag
            if operation == 1:
                update_expr_parts.append(
                    f"#tags.{tag_key} = if_not_exists(#tags.{tag_key}, :zero) + :inc_{tag}"
                )
                expr_attr_values[f":inc_{tag}"] = {"N": str(count)}
            else:
                update_expr_parts.append(
                    f"#tags.{tag_key} = if_not_exists(#tags.{tag_key}, :zero) - :dec_{tag}"
                )
                expr_attr_values[f":dec_{tag}"] = {"N": str(count)}

        update_expression = "SET " + ", ".join(update_expr_parts)

        try:
            dynamodb.update_item(
                TableName=TABLE_NAME,
                Key={
                    "source_path": {"S": source_path},
                    "timestamp": {"S": timestamp}
                },
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expr_attr_names,
                ExpressionAttributeValues=expr_attr_values,
                ConditionExpression="attribute_exists(#sp) AND attribute_exists(#ts)"
            )
            updated_files += 1
        except Exception as e:
            logger.error(f"Failed to update {url}: {str(e)}")
            continue

    return updated_files
