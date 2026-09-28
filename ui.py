from __future__ import annotations
import os
import dearpygui.dearpygui as dpg
from typing import TYPE_CHECKING
from blocks import CATEGORIES, BLOCK_LIBRARY, Block
from generator import validate_python_code

if TYPE_CHECKING:
    from app import VisualBlockEditor

EDITOR: VisualBlockEditor | None = None
dragging_block_id: str | None = None
drag_start_mouse_x: float = 0.0
drag_start_mouse_y: float = 0.0
drag_orig_x: int = 0
drag_orig_y: int = 0

def _apply_theme() -> None:
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (244, 246, 249), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (255, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (220, 225, 232), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
            
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (255, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Header, (232, 238, 245), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (215, 226, 240), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (190, 210, 235), category=dpg.mvThemeCat_Core)
            
            dpg.add_theme_color(dpg.mvThemeCol_Button, (240, 243, 247), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (224, 231, 240), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 214, 230), category=dpg.mvThemeCat_Core)
            
            dpg.add_theme_color(dpg.mvThemeCol_Text, (40, 45, 55), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (248, 250, 252), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (240, 243, 248), category=dpg.mvThemeCat_Core)
            
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (245, 247, 250), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (200, 208, 218), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (175, 185, 198), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 6, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 6, 6, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 6, 4, category=dpg.mvThemeCat_Core)
            
    dpg.bind_theme(global_theme)

    with dpg.theme(tag="run_button_theme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (205, 230, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (180, 215, 250), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (155, 195, 240), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (15, 45, 90), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (150, 195, 245), category=dpg.mvThemeCat_Core)

    with dpg.theme(tag="block_card_theme"):
        with dpg.theme_component(dpg.mvChildWindow):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (43, 53, 68), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (65, 78, 98), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 8, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 1, category=dpg.mvThemeCat_Core)

    with dpg.theme(tag="block_card_selected_theme"):
        with dpg.theme_component(dpg.mvChildWindow):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (53, 68, 90), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (100, 160, 240), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 8, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 2, category=dpg.mvThemeCat_Core)

    with dpg.theme(tag="block_btn_theme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (60, 72, 90), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (80, 95, 118), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (100, 120, 150), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (220, 230, 245), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4, category=dpg.mvThemeCat_Core)

    with dpg.theme(tag="palette_btn_theme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (52, 65, 84), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (70, 86, 110), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (90, 110, 140), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (240, 245, 252), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

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
    grid_color = (236, 240, 245, 255)
    for x in range(0, width, step):
        dpg.draw_line((x, 0), (x, height), color=grid_color, parent=drawlist_tag)
    for y in range(0, height, step):
        dpg.draw_line((0, y), (width, y), color=grid_color, parent=drawlist_tag)


def refresh_workspace_ui() -> None:
    if not EDITOR:
        return

    if dpg.does_item_exist("blocks_container"):
        dpg.delete_item("blocks_container", children_only=True)
    else:
        return

    for index, block in enumerate(EDITOR.blocks):
        _render_block_card(block, index)

    refresh_variables_ui()


def _render_block_card(block: Block, index: int) -> None:
    card_tag = f"workspace_block_{block.id}"
    width = 340
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
        is_selected = (EDITOR and EDITOR.selected_block_id == block.id)
        dpg.bind_item_theme(card_tag, "block_card_selected_theme" if is_selected else "block_card_theme")
        
        with dpg.group(horizontal=True):
            category_icon = "⚙" if block.category == "CONTROL" else "📦"
            
            btn_select = dpg.add_button(
                label=f"{category_icon} {block.label[:22]}",
                width=240,
                height=22,
                callback=lambda s, a, u: (EDITOR.select_block(u), refresh_workspace_ui()),
                user_data=block.id,
            )
            dpg.bind_item_theme(btn_select, "block_btn_theme")
            
            btn_edit = dpg.add_button(
                label="✏",
                width=24,
                height=22,
                callback=lambda s, a, u: _open_block_editor_dialog(u),
                user_data=block.id,
            )
            dpg.bind_item_theme(btn_edit, "block_btn_theme")
            
            btn_del = dpg.add_button(
                label="✕",
                width=24,
                height=22,
                callback=lambda s, a, u: _delete_block_callback(u),
                user_data=block.id,
            )
            dpg.bind_item_theme(btn_del, "block_btn_theme")

        dpg.add_separator()
        
        for line in code_lines:
            stripped = line.strip()
            if stripped.startswith("def ") or stripped.startswith("class ") or stripped.startswith("if ") or stripped.startswith("for ") or stripped.startswith("while "):
                text_color = (255, 255, 255)
            elif stripped.startswith("print(") or stripped.startswith("input("):
                text_color = (130, 220, 140)
            elif "=" in stripped and not stripped.startswith("=="):
                text_color = (245, 210, 130)
            else:
                text_color = (210, 225, 240)
            dpg.add_text(f"  {line}", color=text_color)


def refresh_variables_ui() -> None:
    if not EDITOR or not dpg.does_item_exist("variables_items_group"):
        return

    dpg.delete_item("variables_items_group", children_only=True)
    EDITOR.refresh_variables()
    
    for var_name in EDITOR.variables_list:
        btn = dpg.add_button(
            label=f" 🏷 {var_name} ",
            width=190,
            height=26,
            parent="variables_items_group",
            callback=lambda s, a, u: _on_variable_click(u),
            user_data=var_name,
        )
        dpg.bind_item_theme(btn, "var_chip_theme")


def _on_variable_click(var_name: str) -> None:
    if EDITOR:
        inserted = EDITOR.insert_text_into_selected_block(var_name)
        if not inserted:
            EDITOR.add_block_from_palette(user_data="assign")
            if EDITOR.blocks:
                EDITOR.blocks[-1].code = f"{var_name} = 0"
                EDITOR.blocks[-1].label = f"{var_name} ="
        refresh_workspace_ui()


def _delete_block_callback(block_id: str) -> None:
    if EDITOR and EDITOR.delete_block(block_id):
        refresh_workspace_ui()


def _open_block_editor_dialog(block_id: str) -> None:
    if not EDITOR:
        return
    block = next((b for b in EDITOR.blocks if b.id == block_id), None)
    if not block:
        return

    dialog_tag = "edit_block_modal"
    if dpg.does_item_exist(dialog_tag):
        dpg.delete_item(dialog_tag)

    with dpg.window(
        label=f"Editar Bloque - {block.label}",
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
    if not EDITOR:
        return
    var_name = dpg.get_value("new_var_input") if dpg.does_item_exist("new_var_input") else ""
    var_name = var_name.strip().replace(" ", "_")
    if var_name and var_name not in EDITOR.variables_list:
        EDITOR.variables_list.append(var_name)
        dpg.set_value("new_var_input", "")
        refresh_variables_ui()


def build_interface(editor_instance: VisualBlockEditor) -> None:
    global EDITOR, dragging_block_id, drag_start_mouse_x, drag_start_mouse_y, drag_orig_x, drag_orig_y
    EDITOR = editor_instance

    dpg.create_context()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(base_dir, "LOGO.png")
    ico_path = os.path.join(base_dir, "favicon.ico")

    small_icon_path = ico_path if os.path.exists(ico_path) else (logo_path if os.path.exists(logo_path) else "")
    large_icon_path = ico_path if os.path.exists(ico_path) else (logo_path if os.path.exists(logo_path) else "")

    viewport_kwargs = {
        "title": "🐾 PuRRgramacion - Python visual de bloques",
        "width": 1340,
        "height": 820,
        "resizable": True,
        "min_width": 1100,
        "min_height": 650,
    }
    if small_icon_path:
        viewport_kwargs["small_icon"] = small_icon_path
    if large_icon_path:
        viewport_kwargs["large_icon"] = large_icon_path

    dpg.create_viewport(**viewport_kwargs)

    has_logo = False
    if os.path.exists(logo_path):
        try:
            w, h, c, data = dpg.load_image(logo_path)
            with dpg.texture_registry(show=False):
                dpg.add_static_texture(width=w, height=h, default_value=data, tag="app_logo_texture")
            has_logo = True
        except Exception as e:
            print(f"No se pudo cargar textura de LOGO.png: {e}")

    _apply_theme()

    with dpg.window(
        tag="main_window",
        no_title_bar=True,
        no_move=True,
        no_resize=True,
        no_scrollbar=True,
        no_bring_to_front_on_focus=True,
        pos=(0, 0),
    ):
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

            with dpg.menu(label="Run"):
                dpg.add_menu_item(label="Run Code (Ctrl+R)", callback=_on_run_click)
                dpg.add_menu_item(label="Limpiar Consola", callback=_on_clear_console)

            with dpg.menu(label="Tools"):
                dpg.add_menu_item(label="Ver Codigo Generado", callback=_show_code_viewer_modal)
                dpg.add_menu_item(label="Exportar a script.py", callback=lambda: EDITOR.export_python_file())

        with dpg.group(horizontal=True):
            dpg.add_button(label="📄 New", width=70, height=32, callback=lambda: (EDITOR.clear_workspace(), refresh_workspace_ui()))
            dpg.add_button(label="📂 Open", width=70, height=32, callback=lambda: (EDITOR.load_from_file(), refresh_workspace_ui()))
            dpg.add_button(label="💾 Save", width=70, height=32, callback=lambda: EDITOR.save_to_file())
            
            run_btn = dpg.add_button(label="🐾 Run", width=95, height=32, tag="toolbar_run_btn", callback=_on_run_click)
            dpg.bind_item_theme(run_btn, "run_button_theme")

            dpg.add_button(label="🐞 Debug", width=75, height=32, callback=_show_code_viewer_modal)
            dpg.add_button(label="⚙ Option", width=75, height=32, callback=lambda: None)
            
            dpg.add_spacer(width=620, tag="toolbar_spacer")
            if has_logo:
                dpg.add_image("app_logo_texture", width=36, height=36)
            else:
                dpg.add_text("🐾 🐍", color=(50, 70, 95))

        dpg.add_separator()

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

                for cat_name, cat_data in CATEGORIES.items():
                    with dpg.collapsing_header(label=f"{cat_data['icon']} {cat_name}", default_open=True):
                        items = cat_data["items"]
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
                    dpg.add_text("Workspace (Haz clic y arrastra bloques)", color=(40, 50, 65))
                    dpg.add_spacer(width=340)
                    dpg.add_button(label="📜 Ver Codigo", width=95, callback=_show_code_viewer_modal)

                dpg.add_separator()

                dpg.add_drawlist(width=1600, height=1200, tag="workspace_grid_drawlist")
                _draw_workspace_grid("workspace_grid_drawlist")

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
                dpg.add_text("Haz clic en una variable para\ninsertarla en el bloque activo:", color=(100, 110, 125))
                dpg.add_spacer(height=5)
                
                with dpg.group(tag="variables_items_group"):
                    pass

                dpg.add_spacer(height=10)
                dpg.add_separator()
                dpg.add_text("Agregar Variable:", color=(80, 90, 105))
                dpg.add_input_text(hint="nombre_var", width=190, tag="new_var_input")
                dpg.add_button(label="+ Agregar", width=190, callback=_add_variable_prompt)

        # 4. Bottom Panel: CONSOLE / SALIDA
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

            dpg.add_input_text(
                tag="console_output_display",
                default_value=EDITOR.console_output,
                multiline=True,
                readonly=True,
                width=1285,
                height=90,
            )

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

    # Handlers optimizados para arrastre suave 1:1 con el cursor
    with dpg.handler_registry():
        def _on_mouse_down(sender, app_data):
            global dragging_block_id, drag_start_mouse_x, drag_start_mouse_y, drag_orig_x, drag_orig_y
            mouse_pos = dpg.get_mouse_pos(local=False)
            for b in EDITOR.blocks:
                card_tag = f"workspace_block_{b.id}"
                if dpg.does_item_exist(card_tag) and dpg.is_item_hovered(card_tag):
                    dragging_block_id = b.id
                    EDITOR.select_block(b.id)
                    drag_start_mouse_x, drag_start_mouse_y = mouse_pos
                    drag_orig_x = b.x
                    drag_orig_y = b.y
                    refresh_workspace_ui()
                    break

        def _on_mouse_release(sender, app_data):
            global dragging_block_id
            dragging_block_id = None

        def _on_mouse_move(sender, app_data):
            global dragging_block_id, drag_start_mouse_x, drag_start_mouse_y, drag_orig_x, drag_orig_y
            if dragging_block_id:
                mouse_pos = dpg.get_mouse_pos(local=False)
                dx = mouse_pos[0] - drag_start_mouse_x
                dy = mouse_pos[1] - drag_start_mouse_y
                for b in EDITOR.blocks:
                    if b.id == dragging_block_id:
                        b.x = max(0, int(drag_orig_x + dx))
                        b.y = max(0, int(drag_orig_y + dy))
                        card_tag = f"workspace_block_{b.id}"
                        if dpg.does_item_exist(card_tag):
                            dpg.set_item_pos(card_tag, (b.x, b.y))
                        break

        dpg.add_mouse_down_handler(callback=_on_mouse_down)
        dpg.add_mouse_release_handler(callback=_on_mouse_release)
        dpg.add_mouse_move_handler(callback=_on_mouse_move)

    refresh_workspace_ui()

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
            if dpg.does_item_exist("toolbar_spacer"):
                dpg.set_item_width("toolbar_spacer", max(50, vw - 600))
        except Exception:
            pass

    dpg.set_viewport_resize_callback(_on_viewport_resize)

    dpg.set_primary_window("main_window", True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()