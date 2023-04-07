from pydantic import BaseModel


# Shared properties
class MaintainanceMode(BaseModel):
    id: int
    maintain_status: int


# Properties to receive on item creation
class MaintainanceModeCreate(MaintainanceMode):
    pass


# Properties to receive on item update
class MaintainanceModeUpdate(MaintainanceMode):
    pass


# Properties to return to client
class MaintainanceModeStatus(MaintainanceMode):
    pass
