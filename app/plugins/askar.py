"""Askar plugin for storing and verifying data."""

import hashlib
import json
import logging

from aries_askar import Store
from fastapi import HTTPException

from config import settings


class AskarStorage:
    """Askar storage plugin."""

    def __init__(self):
        """Initialize the Askar storage plugin."""
        self.db = settings.ASKAR_DB
        self.key = Store.generate_raw_key(hashlib.md5(settings.SECRET_KEY.encode()).hexdigest())

    async def provision(self, recreate=False):
        """Provision the Askar storage."""
        await Store.provision(self.db, "raw", self.key, recreate=recreate)

    async def open(self):
        """Open the Askar storage."""
        return await Store.open(self.db, "raw", self.key)

    async def fetch(self, category: str, data_key: str) -> dict | None:
        """Fetch data from the store."""
        store = await self.open()
        try:
            async with store.session() as session:
                data = await session.fetch(category, data_key)
            return json.loads(data.value)
        except Exception:
            logging.debug(f"Error fetching data {category}: {data_key}", exc_info=True)
            return None

    async def store(self, category: str, data_key: str, data: dict, tags: None | dict = None):
        """Store data in the store."""
        store = await self.open()
        try:
            async with store.session() as session:
                await session.insert(category, data_key, json.dumps(data), tags=tags)
        except Exception:
            logging.debug(f"Error storing data {category}: {data_key}", exc_info=True)
            raise HTTPException(status_code=404, detail="Couldn't store record.")

    async def update(self, category: str, data_key: str, data: dict, tags: None | dict = None):
        """Update data in the store."""
        store = await self.open()
        try:
            async with store.session() as session:
                await session.replace(category, data_key, json.dumps(data), tags=tags)
        except Exception:
            logging.debug(f"Error updating data {category}: {data_key}", exc_info=True)
            raise HTTPException(status_code=404, detail="Couldn't update record.")

    async def remove(self, category: str, data_key: str):
        """Remove data from the store."""
        store = await self.open()
        try:
            async with store.session() as session:
                await session.remove(category, data_key)
        except Exception:
            logging.debug(f"Error removing data {category}: {data_key}", exc_info=True)
            raise HTTPException(status_code=404, detail="Couldn't remove record.")
