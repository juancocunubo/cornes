from __future__ import annotations
import os
import sys
import json
import subprocess
from typing import Optional, Callable
from blocks import BLOCK_LIBRARY, Block, build_demo_blocks
from generator import generate_python_from_blocks, extract_identifiers, validate_python_code
import ui

class VisualBlockEditor:
    def __init__(self) -> None:
        self.blocks: list[Block] = build_demo_blocks()
        self.console_output: str = (
            "C:\\Users\\User\\PuRRgramacion> python script.py\n"
            "Dime tu nombre: Juan\n"
            "Hola, Juan!\n"
        )
        self.active_block_id: Optional[str] = None
        self.execution_process: Optional[subprocess.Popen] = None
        self.variables_list: list[str] = ["nombre", "saludar", "salida"]
        self.refresh_variables()

    def refresh_variables(self) -> None:
        """Extracts variables from current blocks to update the floating panel."""
        code = self.generate_code()
        identifiers = extract_identifiers(code)
        all_items = list(dict.fromkeys(
            identifiers["variables"] + identifiers["functions"] + self.variables_list
        ))
        if all_items:
            self.variables_list = all_items

    def add_block_from_palette(self, sender=None, app_data=None, user_data: str = "print") -> Block:
        spec = BLOCK_LIBRARY.get(user_data, {
            "label": f"{user_data}",
            "code": f"# {user_data}",
            "color": (45, 55, 72),
            "category": "CONTROL"
        })
        
        # Calculate staggering position
        base_y = 40 + (len(self.blocks) % 7) * 75
        base_x = 60 + ((len(self.blocks) // 7) * 260) % 500
        
        new_block = Block(
            kind=user_data,
            label=spec["label"],
            code=spec["code"],
            color=spec.get("color", (45, 55, 72)),
            category=spec.get("category", "CONTROL"),
            x=base_x,
            y=base_y,
        )
        self.blocks.append(new_block)
        self.refresh_variables()
        return new_block

    def delete_block(self, block_id: str) -> bool:
        initial_len = len(self.blocks)
        self.blocks = [b for b in self.blocks if b.id != block_id]
        self.refresh_variables()
        return len(self.blocks) < initial_len

    def update_block_code(self, block_id: str, new_code: str) -> None:
        for b in self.blocks:
            if b.id == block_id:
                b.code = new_code
                b.label = new_code.splitlines()[0] if new_code.strip() else b.label
                break
        self.refresh_variables()

    def update_block_pos(self, block_id: str, x: int, y: int) -> None:
        for b in self.blocks:
            if b.id == block_id:
                b.x = max(10, x)
                b.y = max(10, y)
                break

    def clear_workspace(self) -> None:
        self.blocks.clear()
        self.variables_list = ["nombre", "saludar"]
        self.refresh_variables()

    def reset_demo(self) -> None:
        self.blocks = build_demo_blocks()
        self.refresh_variables()

    def generate_code(self) -> str:
        return generate_python_from_blocks(self.blocks)

    def run_code(self, script_input: str = "") -> str:
        """
        Executes the generated Python code and captures output.
        """
        code = self.generate_code()
        is_valid, msg = validate_python_code(code)
        
        header = "C:\\Users\\User\\PuRRgramacion> python script.py\n"
        
        if not is_valid:
            output = f"{header}[SYNTAX ERROR] {msg}\n"
            self.console_output = output
            return output

        try:
            # Run code with current python interpreter
            python_bin = sys.executable
            proc = subprocess.run(
                [python_bin, "-c", code],
                input=script_input if script_input else "Juan\n",
                text=True,
                capture_output=True,
                timeout=10,
                encoding="utf-8",
                errors="replace",
            )
            
            stdout = proc.stdout
            stderr = proc.stderr
            
            output = header
            if script_input:
                output += f"[Input enviado: {script_input.strip()}]\n"
            if stdout:
                output += stdout
            if stderr:
                output += f"\n[Error]:\n{stderr}"
            if not stdout and not stderr:
                output += "[Programa finalizado sin salida.]\n"
                
            self.console_output = output
            return output
        except subprocess.TimeoutExpired:
            self.console_output = f"{header}[TIMEOUT] La ejecucion tardo mas de 10 segundos.\n"
            return self.console_output
        except Exception as e:
            self.console_output = f"{header}[ERROR EJECUCION] {str(e)}\n"
            return self.console_output

    def save_to_file(self, filename: str = "project.purr") -> str:
        data = {
            "version": "1.0",
            "blocks": [b.to_dict() for b in self.blocks],
            "variables": self.variables_list,
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return f"Proyecto guardado en {filename}"

    def load_from_file(self, filename: str = "project.purr") -> bool:
        if not os.path.exists(filename):
            return False
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.blocks = [Block.from_dict(b) for b in data.get("blocks", [])]
        self.variables_list = data.get("variables", ["nombre", "saludar"])
        self.refresh_variables()
        return True

    def export_python_file(self, filename: str = "script.py") -> str:
        code = self.generate_code()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)
        return f"Codigo exportado en {filename}"

    def run(self) -> None:
        ui.build_interface(self)

if __name__ == "__main__":
    app = VisualBlockEditor()
    app.run()
