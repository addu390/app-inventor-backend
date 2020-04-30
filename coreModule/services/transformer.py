import json

from ..constants import JSON_REQUEST
from ..enums import Component
from ..components import InputTextField
from ..serializers import ComponentSerializer


class ApplicationTransformers:
    @staticmethod
    def request_to_map(data):
        component_map = {}
        for x in data[JSON_REQUEST].get("components"):
            print(Component(x.get("component_type")))
            if Component.TEXT_INPUT_FIELD == Component(x.get("component_type")):
                component_map[x.get("uuid")] = InputTextField(x.get("component_type"), x.get("uuid"), x.get("header"),
                                                              x.get("values"), x.get("input_type"), x.get("regex"),
                                                              x.get("placeholder")).__dict__()
        return component_map

    @staticmethod
    def component_request_transformer(components_object):
        components = []
        for component in components_object:
            component_json = ComponentSerializer(component).data
            component_json.update(json.loads(component_json["request"]))
            component_json.pop("request")
            components.append(component_json)
        return components
