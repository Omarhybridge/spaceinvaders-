import os
import importlib.util

spec = importlib.util.spec_from_file_location(
    "clase_ship",
    os.path.join(os.path.dirname(__file__), "clase_Ship.py")
)
clase_ship = importlib.util.module_from_spec(spec)
spec.loader.exec_module(clase_ship)

Ship = clase_ship.Ship
