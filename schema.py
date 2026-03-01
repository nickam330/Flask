import pydantic

from erros import HttpError


class BaseAdv(pydantic.BaseModel):
    title: str
    description: str
    owner: str
    password: str

    @pydantic.field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class CreateAdv(BaseAdv):
    pass


def validate(json_data: dict, schema_cls: type[CreateAdv]) -> dict:
    try:
        schema = schema_cls(**json_data)
        return schema.model_dump(exclude_none=True)
    except pydantic.ValidationError as e:
        errors_descriptions = e.errors()
        for error_description in errors_descriptions:
            error_description.pop("ctx", None)
        raise HttpError(400, errors_descriptions)
