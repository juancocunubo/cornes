from __future__ import annotations
import os
import dearpygui.dearpygui as dpg
from typing import TYPE_CHECKING
from blocks import CATEGORIES, BLOCK_LIBRARY, Block
from generator import validate_python_code

if TYPE_CHECKING:
    from app import VisualBlockEditor

# Global reference for callbacks
EDITOR: VisualBlockEditor | None = None

def _apply_theme() -> None:
    """Creates a clean, modern light theme matching PuRRgramacion screenshot."""
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            # Window & canvas
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (244, 246, 249), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (255, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (220, 225, 232), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
            
            # Headers & Menus
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (255, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Header, (232, 238, 245), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (215, 226, 240), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (190, 210, 235), category=dpg.mvThemeCat_Core)
            
            # Buttons
            dpg.add_theme_color(dpg.mvThemeCol_Button, (240, 243, 247), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (224, 231, 240), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 214, 230), category=dpg.mvThemeCat_Core)
            
            # Text & Inputs
            dpg.add_theme_color(dpg.mvThemeCol_Text, (40, 45, 55), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (248, 250, 252), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (240, 243, 248), category=dpg.mvThemeCat_Core)
            
            # Scrollbars & Rounding
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (245, 247, 250), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (200, 208, 218), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (175, 185, 198), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 6, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 6, 6, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 6, 4, category=dpg.mvThemeCat_Core)
            
    dpg.bind_theme(global_theme)

    # Accent theme for RUN button (matches light blue cat paw toolbar in screenshot)
    with dpg.theme(tag="run_button_theme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (205, 230, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (180, 215, 250), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (155, 195, 240), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (15, 45, 90), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (150, 195, 245), category=dpg.mvThemeCat_Core)

    # Theme for dark visual blocks on workspace (matches dark slate blocks in screenshot)
    with dpg.theme(tag="block_card_theme"):
        with dpg.theme_component(dpg.mvChildWindow):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (43, 53, 68), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (65, 78, 98), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 8, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 1, category=dpg.mvThemeCat_Core)

    # Theme for mini block buttons on workspace
    with dpg.theme(tag="block_btn_theme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (60, 72, 90), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (80, 95, 118), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (100, 120, 150), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (220, 230, 245), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4, category=dpg.mvThemeCat_Core)

    # Theme for palette category buttons
    with dpg.theme(tag="palette_btn_theme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (52, 65, 84), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (70, 86, 110), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (90, 110, 140), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (240, 245, 252), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

    # Theme for variable chip items
    with dpg.theme(tag="var_chip_theme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (220, 235, 252), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (200, 222, 248), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (180, 210, 242), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (25, 60, 110), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (175, 205, 240), category=dpg.mvThemeCat_Core)


def _draw_workspace_grid(drawlist_tag: str, width: int = 2000, height: int = 1600, step: int = 30) -> None:
    """Draws a subtle graph paper grid like in the screenshot."""
    grid_color = (236, 240, 245, 255)
    for x in range(0, width, step):
        dpg.draw_line((x, 0), (x, height), color=grid_color, parent=drawlist_tag)
    for y in range(0, height, step):
        dpg.draw_line((0, y), (width, y), color=grid_color, parent=drawlist_tag)


def refresh_workspace_ui() -> None:
    """Rebuilds the visual blocks on the workspace."""
    if not EDITOR:
        return

    # Clear previous blocks
    if dpg.does_item_exist("blocks_container"):
        dpg.delete_item("blocks_container", children_only=True)
    else:
        return

    for index, block in enumerate(EDITOR.blocks):
        _render_block_card(block, index)

    # Also refresh variables panel
    refresh_variables_ui()


def _render_block_card(block: Block, index: int) -> None:
    """Renders an individual visual python block matching the screenshot."""
    card_tag = f"workspace_block_{block.id}"
    width = 340
    # Estimate height based on code lines
    code_lines = block.code.strip().splitlines()
    line_count = max(len(code_lines), 1)
    height = max(80, 52 + line_count * 20)

    with dpg.child_window(
        width=width,
        height=height,
        pos=(block.x, block.y),
        tag=card_tag,
        parent="blocks_container",
        no_scrollbar=True,
    ):
        dpg.bind_item_theme(card_tag, "block_card_theme")
        
        # Header row with notch label and controls
        with dpg.group(horizontal=True):
            # Category indicator pill
            category_icon = "⚙" if block.category == "CONTROL" else "📦"
            dpg.add_text(f"{category_icon} {block.label[:24]}", color=(255, 255, 255))
            
            dpg.add_spacer(width=20)
            # Edit button
            btn_edit = dpg.add_button(
                label="✏",
                width=24,
                height=20,
                callback=lambda s, a, u: _open_block_editor_dialog(u),
                user_data=block.id,
            )
            dpg.bind_item_theme(btn_edit, "block_btn_theme")
            
            # Delete button
            btn_del = dpg.add_button(
                label="✕",
                width=24,
                height=20,
                callback=lambda s, a, u: _delete_block_callback(u),
                user_data=block.id,
            )
            dpg.bind_item_theme(btn_del, "block_btn_theme")

        dpg.add_separator()
        
        # Syntax formatted code snippet
        for line in code_lines:
            stripped = line.strip()
            # Color syntax matching screenshot
            if stripped.startswith("def ") or stripped.startswith("class ") or stripped.startswith("if ") or stripped.startswith("for ") or stripped.startswith("while "):
                text_color = (255, 255, 255)
            elif stripped.startswith("print(") or stripped.startswith("input("):
                text_color = (130, 220, 140)  # Greenish
            elif "=" in stripped and not stripped.startswith("=="):
                text_color = (245, 210, 130)  # Golden/Warm
            else:
                text_color = (210, 225, 240)  # Light blue/white
            dpg.add_text(f"  {line}", color=text_color)


def refresh_variables_ui() -> None:
    """Updates the 'Variables y Objetos' panel items."""
    if not EDITOR or not dpg.does_item_exist("variables_items_group"):
        return

    dpg.delete_item("variables_items_group", children_only=True)
    EDITOR.refresh_variables()
    
    for var_name in EDITOR.variables_list:
        btn = dpg.add_button(
            label=f" {var_name} ",
            width=190,
            height=26,
            parent="variables_items_group",
            callback=lambda s, a, u: _on_variable_click(u),
            user_data=var_name,
        )
        dpg.bind_item_theme(btn, "var_chip_theme")


def _on_variable_click(var_name: str) -> None:
    """Inserts a variable assignment or usage into console/editor."""
    if EDITOR:
        EDITOR.add_block_from_palette(user_data="assign")
        # Rename latest block's code to this variable
        if EDITOR.blocks:
            EDITOR.blocks[-1].code = f"{var_name} = 0"
            EDITOR.blocks[-1].label = f"{var_name} ="
            refresh_workspace_ui()


def _delete_block_callback(block_id: str) -> None:
    if EDITOR and EDITOR.delete_block(block_id):
        refresh_workspace_ui()


def _open_block_editor_dialog(block_id: str) -> None:
    """Opens modal window to edit Python statements of a block directly."""
    if not EDITOR:
        return
    block = next((b for b in EDITOR.blocks if b.id == block_id), None)
    if not block:
        return

    dialog_tag = "edit_block_modal"
    if dpg.does_item_exist(dialog_tag):
        dpg.delete_item(dialog_tag)

    with dpg.window(
        label=f"Editar Sentencia Python - {block.label}",
        tag=dialog_tag,
        modal=True,
        width=520,
        height=340,
        pos=(450, 200),
        no_collapse=True,
    ):
        dpg.add_text("Codigo Python del Bloque:")
        input_tag = "edit_block_code_input"
        dpg.add_input_text(
            default_value=block.code,
            multiline=True,
            width=490,
            height=180,
            tag=input_tag,
            tab_input=True,
        )
        
        with dpg.group(horizontal=True):
            dpg.add_text("Posicion X:")
            pos_x_tag = "edit_pos_x"
            dpg.add_input_int(default_value=block.x, width=90, tag=pos_x_tag, step=10)
            dpg.add_text("Posicion Y:")
            pos_y_tag = "edit_pos_y"
            dpg.add_input_int(default_value=block.y, width=90, tag=pos_y_tag, step=10)

        dpg.add_separator()
        with dpg.group(horizontal=True):
            def _save_changes():
                new_code = dpg.get_value(input_tag)
                new_x = dpg.get_value(pos_x_tag)
                new_y = dpg.get_value(pos_y_tag)
                EDITOR.update_block_code(block_id, new_code)
                EDITOR.update_block_pos(block_id, new_x, new_y)
                dpg.delete_item(dialog_tag)
                refresh_workspace_ui()

            dpg.add_button(label="Guardar Cambios", width=140, callback=lambda: _save_changes())
            dpg.add_button(label="Cancelar", width=90, callback=lambda: dpg.delete_item(dialog_tag))


def _on_run_click() -> None:
    """Executes python code and updates console."""
    if not EDITOR:
        return
    custom_input = dpg.get_value("console_input_text") if dpg.does_item_exist("console_input_text") else ""
    output = EDITOR.run_code(script_input=custom_input)
    if dpg.does_item_exist("console_output_display"):
        dpg.set_value("console_output_display", output)


def _on_clear_console() -> None:
    if EDITOR:
        EDITOR.console_output = "C:\\Users\\User\\PuRRgramacion> python script.py\n"
        if dpg.does_item_exist("console_output_display"):
            dpg.set_value("console_output_display", EDITOR.console_output)


def _show_code_viewer_modal() -> None:
    """Displays generated python script in a popup window."""
    if not EDITOR:
        return
    code = EDITOR.generate_code()
    modal_tag = "code_preview_modal"
    if dpg.does_item_exist(modal_tag):
        dpg.delete_item(modal_tag)

    with dpg.window(
        label="Codigo Python Generado (script.py)",
        tag=modal_tag,
        modal=True,
        width=650,
        height=450,
        pos=(350, 150),
        no_collapse=True,
    ):
        dpg.add_input_text(default_value=code, multiline=True, width=620, height=340, readonly=True)
        with dpg.group(horizontal=True):
            def _export():
                msg = EDITOR.export_python_file("script.py")
                dpg.set_value("console_output_display", f"[EXPORT] {msg}\n" + EDITOR.console_output)
                dpg.delete_item(modal_tag)

            dpg.add_button(label="Exportar a script.py", width=160, callback=lambda: _export())
            dpg.add_button(label="Cerrar", width=90, callback=lambda: dpg.delete_item(modal_tag))


def _add_variable_prompt() -> None:
    """Adds a new variable from the input field in 'Variables y Objetos'."""
    if not EDITOR:
        return
    var_name = dpg.get_value("new_var_input") if dpg.does_item_exist("new_var_input") else ""
    var_name = var_name.strip().replace(" ", "_")
    if var_name and var_name not in EDITOR.variables_list:
        EDITOR.variables_list.append(var_name)
        dpg.set_value("new_var_input", "")
        refresh_variables_ui()


def build_interface(editor_instance: VisualBlockEditor) -> None:
    """Constructs the full PuRRgramacion GUI matching the screenshot."""
    global EDITOR
    EDITOR = editor_instance

    dpg.create_context()
    dpg.create_viewport(
        title="🐾 PuRRgramacion - Python visual de bloques",
        width=1340,
        height=820,
        resizable=True,
        min_width=1100,
        min_height=650,
    )

    _apply_theme()

    # Main full-screen window container
    with dpg.window(
        tag="main_window",
        no_title_bar=True,
        no_move=True,
        no_resize=True,
        no_scrollbar=True,
        no_bring_to_front_on_focus=True,
        pos=(0, 0),
    ):
        # 1. Menu Bar
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="New (Ctrl+N)", callback=lambda: (EDITOR.clear_workspace(), refresh_workspace_ui()))
                dpg.add_menu_item(label="Open... (Ctrl+O)", callback=lambda: (EDITOR.load_from_file(), refresh_workspace_ui()))
                dpg.add_menu_item(label="Save (Ctrl+S)", callback=lambda: EDITOR.save_to_file())
                dpg.add_separator()
                dpg.add_menu_item(label="Exit", callback=lambda: dpg.stop_dearpygui())

            with dpg.menu(label="Edit"):
                dpg.add_menu_item(label="Restablecer Demo", callback=lambda: (EDITOR.reset_demo(), refresh_workspace_ui()))
                dpg.add_menu_item(label="Limpiar Workspace", callback=lambda: (EDITOR.clear_workspace(), refresh_workspace_ui()))

            with dpg.menu(label="View"):
                dpg.add_menu_item(label="Restablecer Posiciones", callback=lambda: (EDITOR.reset_demo(), refresh_workspace_ui()))

            with dpg.menu(label="Run"):
                dpg.add_menu_item(label="Run Code (Ctrl+R)", callback=_on_run_click)
                dpg.add_menu_item(label="Limpiar Consola", callback=_on_clear_console)

            with dpg.menu(label="Tools"):
                dpg.add_menu_item(label="Ver Codigo Generado", callback=_show_code_viewer_modal)
                dpg.add_menu_item(label="Exportar a script.py", callback=lambda: EDITOR.export_python_file())

            with dpg.menu(label="Help"):
                dpg.add_menu_item(label="Acerca de PuRRgramacion", callback=lambda: None)

        # 2. Top Toolbar (New, Open, Save, 🐾 Run, Debug, Option, 🐾 🐍)
        with dpg.group(horizontal=True):
            dpg.add_button(label="📄 New", width=70, height=32, callback=lambda: (EDITOR.clear_workspace(), refresh_workspace_ui()))
            dpg.add_button(label="📂 Open", width=70, height=32, callback=lambda: (EDITOR.load_from_file(), refresh_workspace_ui()))
            dpg.add_button(label="💾 Save", width=70, height=32, callback=lambda: EDITOR.save_to_file())
            
            # RUN BUTTON (Highlighted light blue with cat paw)
            run_btn = dpg.add_button(label="🐾 Run", width=95, height=32, tag="toolbar_run_btn", callback=_on_run_click)
            dpg.bind_item_theme(run_btn, "run_button_theme")

            dpg.add_button(label="🐞 Debug", width=75, height=32, callback=_show_code_viewer_modal)
            dpg.add_button(label="⚙ Option", width=75, height=32, callback=lambda: None)
            
            # Right branding matching screenshot
            dpg.add_spacer(width=680)
            dpg.add_text("🐾 🐍", color=(50, 70, 95))

        dpg.add_separator()

        # 3. Middle Area (Block Palette on left, Workspace in center, Variables on top right)
        with dpg.group(horizontal=True):
            
            # --- LEFT SIDEBAR: BLOCK PALETTE ---
            with dpg.child_window(
                label="Block Palette",
                width=240,
                height=480,
                border=True,
                tag="palette_window",
            ):
                with dpg.group(horizontal=True):
                    dpg.add_text("Block Palette", color=(40, 50, 65))
                    dpg.add_spacer(width=70)
                    dpg.add_text("✕", color=(150, 160, 175))

                dpg.add_separator()

                # Render all palette categories matching screenshot
                for cat_name, cat_data in CATEGORIES.items():
                    with dpg.collapsing_header(label=f"{cat_data['icon']} {cat_name}", default_open=True):
                        items = cat_data["items"]
                        
                        # OPERADORES inline grid
                        if cat_name == "OPERADORES":
                            with dpg.group(horizontal=True):
                                for key in ["op_add", "op_sub", "op_mul", "op_div"]:
                                    spec = items[key]
                                    btn = dpg.add_button(
                                        label=spec["label"],
                                        width=42,
                                        height=28,
                                        callback=lambda s, a, u: (EDITOR.add_block_from_palette(user_data=u), refresh_workspace_ui()),
                                        user_data=key,
                                    )
                                    dpg.bind_item_theme(btn, "palette_btn_theme")
                            with dpg.group(horizontal=True):
                                for key in ["op_eq", "op_neq", "op_lt", "op_gt"]:
                                    spec = items[key]
                                    btn = dpg.add_button(
                                        label=spec["label"],
                                        width=42,
                                        height=28,
                                        callback=lambda s, a, u: (EDITOR.add_block_from_palette(user_data=u), refresh_workspace_ui()),
                                        user_data=key,
                                    )
                                    dpg.bind_item_theme(btn, "palette_btn_theme")
                            with dpg.group(horizontal=True):
                                for key in ["op_and", "op_or", "op_not"]:
                                    spec = items[key]
                                    btn = dpg.add_button(
                                        label=spec["label"],
                                        width=58,
                                        height=28,
                                        callback=lambda s, a, u: (EDITOR.add_block_from_palette(user_data=u), refresh_workspace_ui()),
                                        user_data=key,
                                    )
                                    dpg.bind_item_theme(btn, "palette_btn_theme")
                                    
                        elif cat_name == "DATOS":
                            with dpg.group(horizontal=True):
                                for key in ["str_data", "int_data", "float_data"]:
                                    spec = items[key]
                                    btn = dpg.add_button(
                                        label=spec["label"],
                                        width=60,
                                        height=28,
                                        callback=lambda s, a, u: (EDITOR.add_block_from_palette(user_data=u), refresh_workspace_ui()),
                                        user_data=key,
                                    )
                                    dpg.bind_item_theme(btn, "palette_btn_theme")
                            with dpg.group(horizontal=True):
                                for key in ["bool_data", "none_data", "list_data"]:
                                    spec = items[key]
                                    btn = dpg.add_button(
                                        label=spec["label"],
                                        width=60,
                                        height=28,
                                        callback=lambda s, a, u: (EDITOR.add_block_from_palette(user_data=u), refresh_workspace_ui()),
                                        user_data=key,
                                    )
                                    dpg.bind_item_theme(btn, "palette_btn_theme")

                        else:
                            # Standard full-width category buttons
                            for key, spec in items.items():
                                btn = dpg.add_button(
                                    label=spec["label"],
                                    width=200,
                                    height=30,
                                    callback=lambda s, a, u: (EDITOR.add_block_from_palette(user_data=u), refresh_workspace_ui()),
                                    user_data=key,
                                )
                                dpg.bind_item_theme(btn, "palette_btn_theme")

            # --- CENTER: WORKSPACE CANVAS ---
            with dpg.child_window(
                label="Workspace",
                width=830,
                height=480,
                border=True,
                tag="workspace_child",
            ):
                with dpg.group(horizontal=True):
                    dpg.add_text("Workspace", color=(40, 50, 65))
                    dpg.add_spacer(width=600)
                    # Quick action to view code
                    dpg.add_button(label="📜 Ver Codigo", width=95, callback=_show_code_viewer_modal)

                dpg.add_separator()

                # Drawing layer for graph paper grid background
                dpg.add_drawlist(width=1600, height=1200, tag="workspace_grid_drawlist")
                _draw_workspace_grid("workspace_grid_drawlist")

                # Container child window where movable blocks live
                with dpg.child_window(
                    tag="blocks_container",
                    width=800,
                    height=410,
                    border=False,
                    pos=(10, 35),
                ):
                    pass

            # --- RIGHT PANEL: VARIABLES Y OBJETOS ---
            with dpg.child_window(
                label="Variables y Objetos",
                width=230,
                height=480,
                border=True,
                tag="variables_window",
            ):
                with dpg.group(horizontal=True):
                    dpg.add_text("Variables y Objetos", color=(40, 50, 65))
                    dpg.add_spacer(width=40)
                    dpg.add_text("✕", color=(150, 160, 175))

                dpg.add_separator()
                
                # Active variables list matching screenshot
                with dpg.group(tag="variables_items_group"):
                    pass

                dpg.add_spacer(height=20)
                dpg.add_separator()
                dpg.add_text("Agregar Variable:", color=(80, 90, 105))
                dpg.add_input_text(hint="nombre_var", width=190, tag="new_var_input")
                dpg.add_button(label="+ Agregar", width=190, callback=_add_variable_prompt)

        # 4. Bottom Panel: CONSOLE / SALIDA (Monospace terminal)
        with dpg.child_window(
            label="Console/Salida",
            width=1310,
            height=200,
            border=True,
            tag="console_window",
        ):
            with dpg.group(horizontal=True):
                dpg.add_text("Console/Salida", color=(40, 50, 65))
                dpg.add_spacer(width=20)
                dpg.add_button(label="🐾 Ejecutar", width=85, height=22, callback=_on_run_click)
                dpg.add_button(label="🧹 Limpiar", width=75, height=22, callback=_on_clear_console)
                dpg.add_spacer(width=850)
                dpg.add_text("✕", color=(150, 160, 175))

            dpg.add_separator()

            # Terminal Display Area
            dpg.add_input_text(
                tag="console_output_display",
                default_value=EDITOR.console_output,
                multiline=True,
                readonly=True,
                width=1285,
                height=90,
            )

            # Interactive Input row for input()
            with dpg.group(horizontal=True):
                dpg.add_text("> Input para input():", color=(60, 70, 85))
                dpg.add_input_text(
                    hint="Texto para responder a input() (ej. Juan)",
                    width=400,
                    tag="console_input_text",
                    default_value="Juan",
                    on_enter=True,
                    callback=lambda: _on_run_click(),
                )
                dpg.add_button(label="Enviar Input y Ejecutar", width=180, callback=_on_run_click)

    # Initial population of workspace blocks and variables
    refresh_workspace_ui()

    # Viewport resize callback to keep layout responsive
    def _on_viewport_resize(sender, app_data):
        try:
            vw = int(dpg.get_viewport_client_width())
            vh = int(dpg.get_viewport_client_height())
            available_w = max(900, vw - 35)
            dpg.set_item_width("console_window", available_w)
            dpg.set_item_width("console_output_display", available_w - 25)
            center_w = max(450, available_w - 490)
            dpg.set_item_width("workspace_child", center_w)
            dpg.set_item_width("blocks_container", center_w - 20)
        except Exception:
            pass

    dpg.set_viewport_resize_callback(_on_viewport_resize)

    dpg.set_primary_window("main_window", True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
