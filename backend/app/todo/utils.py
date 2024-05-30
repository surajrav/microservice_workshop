#!/usr/bin/env python3
# Author: Suraj Ravichandran
# 05/29/2024
import os
import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
UUID4_REGEX_PATTERN = r"^[0-9(a-f|A-F)]{8}-[0-9(a-f|A-F)]{4}-4[0-9(a-f|A-F)]{3}-[89ab][0-9(a-f|A-F)]{3}-[0-9(a-f|A-F)]{12}$"


async def get_mongodb_connection(db_name: str = None):
    db_name = db_name or os.environ['DB_NAME']
    mongo_uri = f"mongodb://{os.environ['DB_USER']}:{os.environ['DB_PASS']}@{os.environ['DB_HOST']}:27017/{db_name}"
    db_client = AsyncIOMotorClient(mongo_uri, server_api=ServerApi('1'), uuidRepresentation="standard")
    db_handle = db_client[db_name]
    return db_client, db_handle


def collect_parameters(keys):
    """
    Ensure that we have all necessary environment variables based on a list of keys
    :param keys: A list of environment variable names
    """
    for key in keys:
        if key not in os.environ:
            raise SystemError(f'Missing environment variable: {key}')


def get_utcnow():
    """
    Get a string representing UTC now already preformatted with the desired output format
    :return: string
    """
    return datetime.datetime.now(datetime.timezone.utc).strftime(DATETIME_FORMAT)
