#!/usr/bin/env python3
# Author: Suraj Ravichandran
# 05/29/2024
from . import models


FIXTURE_DATA = [
    {
        "first_name": "Suraj",
        "last_name": "Ravichandran",
        "username": "surajravi"
    },
    {
        "first_name": "Aniket",
        "last_name": "Sharma",
        "username": "asharma"
    },
    {
        "first_name": "Luckas",
        "last_name": "Friendel",
        "username": "luckas_friendel"
    }
]


async def populate_fixtures(db_client):
    """
    Checks if the database is empty and if so populates it with the predefined fixtures from this file
    (see `FIXTURE_DATA` in this file for data).
    """
    if await db_client.users.estimated_document_count():
        # This database has been populated so no need to re-init with fixture data
        return
    else:
        for entity_data in FIXTURE_DATA:
            # This step of parsing into the pydanctic model below ensures the data/schema integrity
            # so even though we get back to dict post this, it is useful
            user = models.User.model_validate(entity_data)
            user_data = user.model_dump(by_alias=True)
            _new_user = await db_client.users.insert_one(user_data)
