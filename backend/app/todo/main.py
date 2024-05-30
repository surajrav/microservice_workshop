#!/usr/bin/env python3
# Author: Suraj Ravichandran
# 05/29/2024
import os
import datetime
import uuid
from contextlib import asynccontextmanager
from typing import Annotated, Union
from fastapi import FastAPI, Path, File, Form, UploadFile, HTTPException
from . import utils


# before we initiate the FastAPI app ensure that we have all the required environment (mongodb info, etc)
# and if not then this util function should raise a system error (fail with required info early)
utils.collect_parameters([
    "DB_NAME", "DB_HOST", "DB_USER", "DB_PASS", "DB_COLLECTION_NAME"
])


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown operations
    """
    # Operations to perform prior to whence the app starts taking requests

    # Motor (mongo's async python client) setup
    app.mongodb_client, app.mongodb = await utils.get_mongodb_connection()

    # Populate with initial data if db empty
    # await fixtures.populate_fixtures(app.mongodb)

    # This yields execution back to the FastAPI which starts taking requests
    yield

    # Any shutdown cleanup and resource clearance should go here
    app.mongodb_client.close()


# Establish the FastAPI app
app = FastAPI(lifespan=lifespan)



@app.get(
    "/",
    response_description="List all todo tasks"
)
async def list_todo_tasks():
    """
    This endpoint provides a list todo task entities enough for the consumer to search through
    """
    return [
        {
            "id": "6eb8745c-0b92-407e-9c65-02b85e9386c1",
            "username": "surajravi",
            "todos": [
                "Curate Workshop",
                "Demo",
                "Gather Feedback"
            ]
        },
        {
            "id": "0fc950e1-17ac-4844-ae60-5b63b7878c37",
            "username": "asharma",
            "todos": [
                "Vote",
                "Buy Milk",
                "Paint House"
            ]

        }
    ]

