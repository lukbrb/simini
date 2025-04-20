import sys
from dataclasses import dataclass
from enum import Enum

class PositiveInt:
    def __init__(self, value: int):
        if value <= 0:
            raise ValueError("Value must be a positive integer.")
        self.value = value

    def __int__(self):
        return self.value

    def __repr__(self):
        return f"PositiveInt({self.value})"


class PositiveFloat:
    def __init__(self, value: float):
        if value <= 0.0:
            raise ValueError("Value must be a positive float.")
        self.value = value

    def __float__(self):
        return self.value

    def __repr__(self):
        return f"PositiveFloat({self.value})"


IntInf= sys.maxsize
FloatInf = sys.float_info.max

class IntRange(int):
    def __new__(cls, value: int, min_value: int= -IntInf, max_value: int=IntInf):
        if not (min_value <= value <= max_value):
            raise ValueError(f"Value must be between {min_value} and {max_value}.")
        instance = super().__new__(cls, value)
        instance.min_value = min_value
        instance.max_value = max_value
        return instance

    def __repr__(self):
        return f"{int(self)}, from [{self.min_value} ; {self.max_value}]"

    def __next__(self):
        return self.__class__(self + 1, self.min_value, self.max_value) if (self + 1) <= self.max_value else self.__class__(self, self.min_value, self.max_value)
    
    def prev(self):
        return self.__class__(self - 1, self.min_value, self.max_value) if (self - 1) >= self.min_value else self.__class__(self, self.min_value, self.max_value)


class FloatRange(float):
    def __new__(cls, value: float, min_value: float= -FloatInf, max_value: float=FloatInf):
        if not (min_value <= value <= max_value):
            raise ValueError(f"Value must be between {min_value} and {max_value}.")
        instance = super().__new__(cls, value)
        instance.min_value = min_value
        instance.max_value = max_value
        return instance

    def __repr__(self):
        return f"{float(self):.3f}, from [{self.min_value} ; {self.max_value}]"

    def __next__(self):
        return self.__class__(self + 0.1, self.min_value, self.max_value) if (self + 0.1) <= self.max_value else self.__class__(self, self.min_value, self.max_value)
    
    def prev(self):
        return self.__class__(self - 0.1, self.min_value, self.max_value) if (self - 0.1) >= self.min_value else self.__class__(self, self.min_value, self.max_value)


# class PositiveIntRange(IntRange):
#     def __new__(cls, value: int, min_value: int= 0, max_value: int=IntInf):
#         if not (min_value <= value <= max_value):
#             raise ValueError(f"Value must be between {min_value} and {max_value}.")
#         return super().__new__(cls, value, min_value, max_value)


# class PositiveFloatRange(FloatRange):
#     def __new__(cls, value: float, min_value: float= 0.0, max_value: float=FloatInf):
#         if not (min_value <= value <= max_value):
#             raise ValueError(f"Value must be between {min_value} and {max_value}.")
#         return super().__new__(cls, value, min_value, max_value)


class MultipleChoice:
    def __init__(self, choices: list[str], default: str = None):
        self.choices = choices
        self.value = default
        if default is not None and default not in choices:
            raise ValueError(f"Default value '{default}' is not in the choices.")
        if default is None:
            self.value = choices[0] if choices else None
        self.selected_index = choices.index(self.value) if self.value in choices else 0
        self.selected_value = self.choices[self.selected_index]
        if not self.choices:
            raise ValueError("Choices list cannot be empty.")
        if not isinstance(self.choices, list):
            raise TypeError("Choices must be a list.")

    def __next__(self):
        self.selected_index = (self.selected_index + 1) % len(self.choices)
        self.selected_value = self.choices[self.selected_index]
        return self.__class__(choices= self.choices, default=self.selected_value)
    
    def prev(self):
        self.selected_index = (self.selected_index - 1) % len(self.choices)
        self.selected_value = self.choices[self.selected_index]
        return self.__class__(choices= self.choices, default=self.selected_value)
    
    def __repr__(self):
        return f"{self.selected_value} from [{', '.join(self.choices)}]"
    
class Boolean(MultipleChoice):
    def __init__(self, default):
        super().__init__(choices=[True, False], default=default)
        self.value = default
        self.selected_value = self.choices[self.selected_index]
    
    def __next__(self):
        self.selected_index = (self.selected_index + 1) % len(self.choices)
        self.selected_value = self.choices[self.selected_index]
        return self.__class__(default=self.selected_value)
    
    def prev(self):
        self.selected_index = (self.selected_index - 1) % len(self.choices)
        self.selected_value = self.choices[self.selected_index]
        return self.__class__(default=self.selected_value)
    def __repr__(self):
        return "ON" if self.selected_value else "OFF"