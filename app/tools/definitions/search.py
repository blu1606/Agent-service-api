from pydantic import BaseModel, Field

class WebSearchInput(BaseModel):
    input:str = Field(description="Content that needed to be searched on the internet to get answer")
