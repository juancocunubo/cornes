from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any
import uuid

@dataclass
class Block:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    kind: str = ""
    label: str = ""
    code: str = ""
    category: str = "CONTROL"
    color: tuple[int, int, int] = (45, 55, 72)
    x: int = 0
    y: int = 0
    children: List["Block"] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "label": self.label,
            "code": self.code,
            "category": self.category,
            "color": list(self.color),
            "x": self.x,
            "y": self.y,
            "children": [c.to_dict() for c in self.children],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Block":
        return cls(
            id=data.get("id", str(uuid.uuid4())[:8]),
            kind=data.get("kind", ""),
            label=data.get("label", ""),
            code=data.get("code", ""),
            category=data.get("category", "CONTROL"),
            color=tuple(data.get("color", [45, 55, 72])),
            x=data.get("x", 0),
            y=data.get("y", 0),
            children=[cls.from_dict(c) for c in data.get("children", [])],
        )

# Categorized Palette matching PuRRgramacion screenshot
CATEGORIES = {
    "CONTROL": {
        "color": (50, 68, 92),
        "icon": "⚙",
        "items": {
            "if": {"label": "if condition:", "code": "if condicion:\n    pass", "color": (50, 68, 92)},
            "else": {"label": "else:", "code": "else:\n    pass", "color": (50, 68, 92)},
            "elif": {"label": "elif condition:", "code": "elif condicion:\n    pass", "color": (50, 68, 92)},
            "for": {"label": "for i in range():", "code": "for i in range(10):\n    print(i)", "color": (50, 68, 92)},
            "while": {"label": "while condition:", "code": "while condicion:\n    pass", "color": (42, 60, 82)},
        }
    },
    "DEFINICIONES": {
        "color": (65, 80, 105),
        "icon": "📦",
        "items": {
            "def": {"label": "def function_name(args):", "code": "def funcion(arg1):\n    return arg1", "color": (52, 73, 94)},
            "class": {"label": "class ClassName:", "code": "class MiClase:\n    def __init__(self):\n        pass", "color": (52, 73, 94)},
            "return": {"label": "return", "code": "return resultado", "color": (70, 92, 118)},
            "yield": {"label": "yield", "code": "yield valor", "color": (70, 92, 118)},
        }
    },
    "VARIABLES Y TIPOS": {
        "color": (110, 85, 55),
        "icon": "🏷",
        "items": {
            "assign": {"label": "variable =", "code": "variable = valor", "color": (115, 88, 55)},
            "int": {"label": "int()", "code": "int(x)", "color": (100, 80, 55)},
            "str": {"label": "str()", "code": "str(x)", "color": (100, 80, 55)},
            "float": {"label": "float()", "code": "float(x)", "color": (100, 80, 55)},
            "bool": {"label": "bool()", "code": "bool(x)", "color": (100, 80, 55)},
            "list": {"label": "list()", "code": "lista = []", "color": (100, 80, 55)},
            "dict": {"label": "dict()", "code": "diccionario = {}", "color": (100, 80, 55)},
            "tuple": {"label": "tuple()", "code": "tupla = ()", "color": (100, 80, 55)},
        }
    },
    "OPERADORES": {
        "color": (72, 85, 99),
        "icon": "⚡",
        "items": {
            "op_add": {"label": "+", "code": "a + b", "color": (70, 80, 95)},
            "op_sub": {"label": "-", "code": "a - b", "color": (70, 80, 95)},
            "op_mul": {"label": "*", "code": "a * b", "color": (70, 80, 95)},
            "op_div": {"label": "/", "code": "a / b", "color": (70, 80, 95)},
            "op_eq": {"label": "==", "code": "a == b", "color": (70, 80, 95)},
            "op_neq": {"label": "!=", "code": "a != b", "color": (70, 80, 95)},
            "op_lt": {"label": "<", "code": "a < b", "color": (70, 80, 95)},
            "op_gt": {"label": ">", "code": "a > b", "color": (70, 80, 95)},
            "op_and": {"label": "and", "code": "cond1 and cond2", "color": (70, 80, 95)},
            "op_or": {"label": "or", "code": "cond1 or cond2", "color": (70, 80, 95)},
            "op_not": {"label": "not", "code": "not condicion", "color": (70, 80, 95)},
        }
    },
    "FUNCIONES": {
        "color": (46, 90, 130),
        "icon": "ƒ",
        "items": {
            "print": {"label": "print()", "code": 'print("Hola")', "color": (46, 90, 130)},
            "input": {"label": "input()", "code": 'nombre = input("Dime tu nombre: ")', "color": (46, 90, 130)},
            "len": {"label": "len()", "code": "len(items)", "color": (46, 90, 130)},
            "abs": {"label": "abs()", "code": "abs(x)", "color": (46, 90, 130)},
            "range": {"label": "range()", "code": "range(10)", "color": (46, 90, 130)},
        }
    },
    "IMPORTACIONES": {
        "color": (78, 65, 110),
        "icon": "📥",
        "items": {
            "import": {"label": "import module_name", "code": "import math", "color": (78, 65, 110)},
            "from_import": {"label": "from module import something", "code": "from math import sqrt", "color": (78, 65, 110)},
        }
    },
    "DATOS": {
        "color": (55, 110, 75),
        "icon": "💎",
        "items": {
            "str_data": {"label": "'hello'", "code": "'hello'", "color": (55, 110, 75)},
            "int_data": {"label": "10", "code": "10", "color": (65, 115, 80)},
            "float_data": {"label": "3.14", "code": "3.14", "color": (65, 115, 80)},
            "bool_data": {"label": "True", "code": "True", "color": (50, 95, 140)},
            "none_data": {"label": "None", "code": "None", "color": (100, 70, 120)},
            "list_data": {"label": "[1, 2, 3]", "code": "[1, 2, 3]", "color": (55, 110, 75)},
        }
    }
}

# Flattened lookup library
BLOCK_LIBRARY: Dict[str, Dict[str, Any]] = {}
for cat_name, cat_data in CATEGORIES.items():
    for item_key, item_spec in cat_data["items"].items():
        BLOCK_LIBRARY[item_key] = {
            **item_spec,
            "category": cat_name,
        }

def build_demo_blocks() -> list[Block]:
    """Generates the demo blocks shown in the screenshot."""
    return [
        Block(
            kind="def",
            label="def saludar(nombre):",
            code='def saludar(nombre):\n    print("Hola, " + nombre + "!")',
            category="DEFINICIONES",
            color=(45, 55, 72),
            x=60,
            y=30,
        ),
        Block(
            kind="if",
            label="if variable_x > 10:",
            code='variable_x = 15\nif variable_x > 10:\n    print("Mayor que 10")',
            category="CONTROL",
            color=(45, 55, 72),
            x=60,
            y=140,
        ),
        Block(
            kind="for",
            label="for i in range(5):",
            code='for i in range(5):\n    print(i)',
            category="CONTROL",
            color=(45, 55, 72),
            x=60,
            y=260,
        ),
        Block(
            kind="input",
            label='nombre = input("Dime tu nombre: ")',
            code='nombre = input("Dime tu nombre: ")\nsaludar("Usuario")',
            category="FUNCIONES",
            color=(45, 55, 72),
            x=60,
            y=370,
        ),
        Block(
            kind="assign",
            label="variable =",
            code='variable = 10',
            category="VARIABLES Y TIPOS",
            color=(45, 55, 72),
            x=440,
            y=240,
        ),
    ]
