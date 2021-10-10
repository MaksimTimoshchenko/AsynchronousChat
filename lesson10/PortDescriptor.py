class PortDescriptor:
    def __init__(self, name, default=None):
        self.name = "_" + name
        self.type = int
        self.default = 7777

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError("Значение должно быть типа %s" % self.type)
        # можно, конечно, добавить в условие "0 < value < 65535", но по ТЗ было требование такое
        elif value < 0:
            raise ValueError("Значение должно быть больше либо равно 0")
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        raise AttributeError("Невозможно удалить атрибут")
