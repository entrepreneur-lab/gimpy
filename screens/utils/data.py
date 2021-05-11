from dataclasses import dataclass

@dataclass
class ImageNames:
    oldname: str
    newname: str = ""
