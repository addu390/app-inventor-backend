class Base(object):
    def __init__(self, component_type, uuid, header, values):
        self.component_type = component_type
        self.uuid = uuid
        self.header = header
        self.values = values

    def __dict__(self):
        return {
            "component_type": self.component_type,
            "uuid": self.uuid,
            "header": self.header,
            "values": self.values
        }


class Button(Base):
    def __init__(self, color, action):
        self.color = color
        self.action = action


class InputTextField(Base):
    def __init__(self, component_type, uuid, header, values, input_type, regex, placeholder):
        super().__init__(component_type, uuid, header, values)
        self.input_type = input_type
        self.regex = regex
        self.placeholder = placeholder

    def __dict__(self):
        super_dict = super().__dict__()
        input_test_dict = {
            "input_type": self.input_type,
            "regex": self.regex,
            "placeholder": self.placeholder
        }
        super_dict.update(input_test_dict)
        return super_dict
