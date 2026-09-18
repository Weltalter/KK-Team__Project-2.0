from pydantic import BaseModel, model_validator


class ApplicationSample(BaseModel):
    title: str = ''
    description: str = ''
    hashtags: list = None

    @model_validator(mode="after")
    def post_init_logic(self):
        self.hashtags = [] if self.hashtags is None else list(self.hashtags)

        return self

class ApplicationLibrary(BaseModel):
    object_list: list[ApplicationSample]
    