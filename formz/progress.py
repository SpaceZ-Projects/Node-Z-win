import clr
import System
import System.Windows.Forms as Forms
import System.Drawing as Drawing

from typing import Tuple, Optional


class ProgressBar(Forms.ProgressBar):
    def __init__(
            self,
            size: Tuple[int, int] = None,
            value: Optional[int] = None,
            location: Tuple[int, int] = (0, 0),
            minvalue: Optional[int] = 0,
            maxvalue: Optional[int] = 100
        ):
        super().__init__()

        self._size = size
        self._value = value
        self._location = location
        self._minvalue = minvalue
        self._maxvalue = maxvalue

        if self._size is None:
            self.AutoSize = True
        else:
            self.AutoSize = False
            self.Size = Drawing.Size(*self._size)

        self.Location = Drawing.Point(*self._location)
        self.Minimum = self._minvalue
        self.Maximum = self._maxvalue
        
        if self._value is not None:
            self.Value = self._value

        self.Style = Forms.ProgressBarStyle(0)

    @property
    def value(self) -> int:
        return self.Value

    @value.setter
    def value(self, new_value: int):
        if self._minvalue <= new_value <= self._maxvalue:
            self.Value = new_value
        else:
            raise ValueError(f"Value must be between {self._minvalue} and {self._maxvalue}")

    @property
    def minvalue(self) -> int:
        return self.Minimum

    @minvalue.setter
    def minvalue(self, new_min: int):
        if new_min < self._maxvalue:
            self.Minimum = new_min
            self._minvalue = new_min
        else:
            raise ValueError("Minimum must be less than maximum")

    @property
    def maxvalue(self) -> int:
        return self.Maximum

    @maxvalue.setter
    def maxvalue(self, new_max: int):
        if new_max > self._minvalue:
            self.Maximum = new_max
            self._maxvalue = new_max
        else:
            raise ValueError("Maximum must be greater than minimum")
