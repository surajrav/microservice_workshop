#!/usr/bin/env python3
# Author: Suraj Ravichandran
# 05/29/2024
import os
import datetime
import uuid
from contextlib import asynccontextmanager
from typing import Annotated, Union
from fastapi import FastAPI, Path, File, Form, UploadFile, HTTPException
from . import utils, models, fixtures


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
    await fixtures.populate_fixtures(app.mongodb)

    # This yields execution back to the FastAPI which starts taking requests
    yield

    # Any shutdown cleanup and resource clearance should go here
    app.mongodb_client.close()


# Establish the FastAPI app
app = FastAPI(lifespan=lifespan)


@app.post(
    "/",
    response_description="Create a new User record",
    response_model=models.User,
    status_code=201,  # for created
    response_model_by_alias=False
)
async def create_user(user: models.UserInput):
    """
    Create a new user record.

    A unique `id` will be created and provided in the response.

    """
    # TODO: Optimize to one call instead of insert_one and find_one
    user_data = user.model_dump(by_alias=True)
    new_user = await app.mongodb.users.insert_one(user_data)
    created_user = await app.mongodb.patients.find_one({"_id": new_user.inserted_id})
    return created_user


@app.get(
    "/{user_id}",
    response_model=models.User,
    response_model_by_alias=False
)
async def get_user(
        user_id: Annotated[str, Path(pattern=utils.UUID4_REGEX_PATTERN, description="The ID of the user whose data to get")]
):
    """
    Retrieve a user's detailed information via the `user_id` parameter specified.
    """
    # Note: First time using the walrus operator for me (Syntactic Sugar FTW!)
    if (user := await app.mongodb.users.find_one({"_id": uuid.UUID(user_id)})) is not None:
        return user
    else:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@app.get(
    "/",
    response_description="List all users",
    response_model=models.UserCollection,
    response_model_by_alias=False
)
async def list_patients():
    """
    This endpoint provides a list user entities enough for the consumer to search through
    and then retrieve a detailed entity via the GET (singular) yser data endpoint using the id obtained here.

    TODO: This is currently non-paginated and limited to the first 1000 records, fix with pagination
    """
    return models.UserCollection(users=await app.mongodb.users.find().to_list(length=1000))


@app.put(
    "/{user_id}",
    response_model=models.User,
    response_model_by_alias=False,
    response_description="Update the specified user's data"
)
async def update_patient(
        user_id: Annotated[str, Path(pattern=utils.UUID4_REGEX_PATTERN, description="The ID of the user to update")],
        user_data: models.UserInput
):
    """
    Update the user's details
    """
    if (user := await app.mongodb.users.find_one({"_id": uuid.UUID(user_id)})) is not None:
        try:
            _result = await app.mongodb.users.update_one({"_id": uuid.UUID(user_id)}, user_data)
            user = await app.mongodb.users.find_one({"_id": uuid.UUID(user_id)})
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    else:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

