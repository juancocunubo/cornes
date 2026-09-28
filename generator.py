from __future__ import annotations
from blocks import Block
import ast
import re

def render_block_code(block: Block) -> str:
    """Returns the executable Python code for a single block."""
    return block.code.strip()

def generate_python_from_blocks(blocks: list[Block]) -> str:
    """
    Generates unified Python script from a list of blocks.
    Blocks are ordered naturally by their vertical (y) position, then horizontal (x).
    """
    if not blocks:
        return "# Workspace vacio\n"

    # Sort blocks primarily by Y coordinate, then X coordinate
    sorted_blocks = sorted(blocks, key=lambda b: (b.y, b.x))

    code_segments: list[str] = []
    for block in sorted_blocks:
        code = render_block_code(block)
        if code:
            code_segments.append(code)

    full_code = "\n\n".join(code_segments) + "\n"
    return full_code

def extract_identifiers(code: str) -> dict[str, list[str]]:
    """
    Analyzes generated code using AST to find defined variables, functions, and classes.
    Returns a dictionary with 'variables', 'functions', and 'classes'.
    """
    results: dict[str, list[str]] = {
        "variables": [],
        "functions": [],
        "classes": [],
    }

    try:
        tree = ast.parse(code)
    except Exception:
        # Fallback to simple regex if code is currently incomplete/invalid syntax
        var_matches = re.findall(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*=", code, re.MULTILINE)
        fn_matches = re.findall(r"^def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", code, re.MULTILINE)
        cls_matches = re.findall(r"^class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[:\(]", code, re.MULTILINE)
        results["variables"] = list(dict.fromkeys(var_matches))
        results["functions"] = list(dict.fromkeys(fn_matches))
        results["classes"] = list(dict.fromkeys(cls_matches))
        return results

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name not in results["functions"]:
                results["functions"].append(node.name)
        elif isinstance(node, ast.ClassDef):
            if node.name not in results["classes"]:
                results["classes"].append(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if target.id not in results["variables"] and target.id not in results["functions"]:
                        results["variables"].append(target.id)

    return results

def validate_python_code(code: str) -> tuple[bool, str]:
    """Validates Python syntax. Returns (is_valid, error_message)."""
    try:
        ast.parse(code)
        return True, "Sintaxis valida."
    except SyntaxError as e:
        return False, f"Error de sintaxis (linea {e.lineno}): {e.msg}"
    except Exception as e:
        return False, f"Error al analizar codigo: {str(e)}"
