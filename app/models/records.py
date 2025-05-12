from pydantic import BaseModel, Field

class DidLogRecord(BaseModel):
    scid: str = Field()
    logHistory: str = Field()

class DidWitnessRecord(BaseModel):
    scid: str = Field()
    witnessFile: list = Field()

class DidResourceRecord(BaseModel):
    scid: str = Field()
    resourcePath: str = Field()
    resourceData: dict = Field()