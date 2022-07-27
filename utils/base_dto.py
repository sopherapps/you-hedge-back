import orjson
from flask import Flask
from pydantic import BaseModel
from pydantic.utils import ROOT_KEY


def orjson_dumps(v, *, default):
    """orjson.dumps returns bytes, to match standard json.dumps we need to decode"""
    return orjson.dumps(v, default=default).decode()


class BaseDto(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        arbitrary_types_allowed = True

    def jsonify(self, app: Flask):
        """Jsonifies the DTO to be returned in a Flask view"""
        return app.response_class(self.bjson(), mimetype=app.config["JSONIFY_MIMETYPE"])

    def bjson(self) -> str:
        """
        Generate a JSON representation of the model as bytes not as string compared to self.json(),
        """
        data = self.dict()
        if self.__custom_root_type__:
            data = data[ROOT_KEY]

        return self.__config__.orjson.dumps(data, default=self.__json_encoder__)
