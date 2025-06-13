from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: str


class UserSchema(UserBase):
    id: int
    class Config:
        from_attributes = True


class UserSchemaInput(UserBase):
    pass
