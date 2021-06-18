from typing import Dict

HUE, SATURATION, VALUE = "HUE", "SATURATION", "VALUE"

HSV:Dict[str,Dict[str,int]] = {
    "RED": {
        HUE: 0, 
        SATURATION: 100, 
        VALUE: 100}, 
    "GREEN": {
        HUE: 120, 
        SATURATION: 100, 
        VALUE: 100}, 
    "BLUE":  {
        HUE: 240, 
        SATURATION: 100, 
        VALUE: 100}}