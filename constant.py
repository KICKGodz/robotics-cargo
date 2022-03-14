from enum import Enum
import numpy as np

class Color(Enum):
     Red = "Red"
     Blue = "Blue"

# (!!!) Change Based on Team Color
TEAM = Color.Blue

# Window Size (DO NOT CHANGE)
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640

# JSON
PROTOCOL = "1.0"
FOV = 69

# Ball Colors (Work for BGR)
LIGHT_BLUE = (100,150,0)
DARK_BLUE = (140,255,255)

# Work for RGB
LIGHT_RED = (115,50,100)
DARK_RED = (160,255,255)

# Balls in Line of Intake
INTAKE_OFFSET = 45