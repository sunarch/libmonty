from pydantic import BaseModel, ValidationError, validator

class UserSubModel(BaseModel):
    name: str
    
    validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()


class UserModel(BaseModel):
    name: str
    username: str
    password1: str
    password2: str
    other: UserSubModel

    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')
        return v

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v
        
    @validator('other')
    def other_list(cls, v):
        assert isinstance(v, UserSubModel), 'must be alphanumeric'
        return v


user_json = {
    "name": 'John Smith',
    "username": 'scolvin',
    "password1": 'zxcvbn',
    "password2": 'zxcvbn',
    "other": {
        "name": "pfgerpogwp"
    }
}

try:
    user = UserModel(**user_json)
except ValidationError as e:
    print(e)

print(user)

print(user.__dict__)

user.password2 = "fwe"

print(user)

print(user.other.name)
