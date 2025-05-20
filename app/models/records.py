from pydantic import BaseModel, Field


class DidLogRecord(BaseModel):
    """Model for a DID log file record."""

    scid: str = Field()
    log_history: str = Field()


class DidWitnessRecord(BaseModel):
    """Model for a DID witness file record."""

    scid: str = Field()
    witness_file: list = Field()


class DidResourceRecord(BaseModel):
    """Model for a DID resource record."""

    scid: str = Field()
    media_type: str = Field()
    resource_path: str = Field()
    resource_data: str = Field()
