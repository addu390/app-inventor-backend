import enum


class Component(enum.Enum):
    TEXT_INPUT_FIELD = 1
    IMAGE_UPLOAD_BUTTON = 2
    RADIO_BUTTON = 3
    MULTI_SELECTION = 4
    SUBMIT_BUTTON = 5


class TextInputFieldType(enum.Enum):
    MULTI_LINE = 1
    SINGLE_LINE = 2
