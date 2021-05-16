from dataclasses import dataclass

@dataclass
class ImageNames:
    filename: str
    class_: str = ""
