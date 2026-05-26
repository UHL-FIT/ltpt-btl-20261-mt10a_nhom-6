import re

with open('views_tk.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Define color mappings for CTk elements (light -> (light, dark))
color_map = {
    '"#ffffff"': '("#ffffff", "#2b2b2b")',
    '"#f8fafc"': '("#f8fafc", "#1e1e1e")',
    '"#0f172a"': '("#0f172a", "#f8fafc")',
    '"#475569"': '("#475569", "#cbd5e1")',
    '"#64748b"': '("#64748b", "#94a3b8")',
    '"#e2e8f0"': '("#e2e8f0", "#3f3f46")',
    '"#cbd5e1"': '("#cbd5e1", "#52525b")',
    '"#334155"': '("#334155", "#e2e8f0")'
}

args_to_replace = ["fg_color", "text_color", "border_color", "button_color", "button_hover_color"]

for arg in args_to_replace:
    for light, tuple_val in color_map.items():
        pattern = rf'{arg}\s*=\s*{light}'
        replacement = f'{arg}={tuple_val}'
        content = re.sub(pattern, replacement, content)

content = content.replace('fg_color=("#0f172a", "#f8fafc")', 'fg_color="#0f172a"')
content = content.replace('text_color=("#ffffff", "#2b2b2b")', 'text_color="#ffffff"')
content = content.replace('fg_color=("#1e293b", "#1e293b")', 'fg_color="#1e293b"')

style_code = """    def change_appearance_mode_event(self, new_appearance_mode: str) -> None:
        \"\"\"Sự kiện chuyển đổi chế độ Sáng/Tối\"\"\"
        ctk.set_appearance_mode(new_appearance_mode)
        
        style = ttk.Style(self)
        if new_appearance_mode == "Dark":
            style.configure("Treeview", background="#2b2b2b", foreground="#f8fafc", rowheight=32, fieldbackground="#2b2b2b", bordercolor="#3f3f46", borderwidth=0, font=("Segoe UI", 10))
            style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#3f3f46", foreground="#f8fafc", relief="flat", padding=5)
            style.map("Treeview", background=[("selected", "#3b82f6")], foreground=[("selected", "#ffffff")])
            style.map("Treeview.Heading", background=[("active", "#52525b")])
        else:
            style.configure("Treeview", background="#ffffff", foreground="#0f172a", rowheight=32, fieldbackground="#ffffff", bordercolor="#e2e8f0", borderwidth=0, font=("Segoe UI", 10))
            style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#f1f5f9", foreground="#0f172a", relief="flat", padding=5)
            style.map("Treeview", background=[("selected", "#3b82f6")], foreground=[("selected", "#ffffff")])
            style.map("Treeview.Heading", background=[("active", "#e2e8f0")])
"""

content = re.sub(
    r'    def change_appearance_mode_event\(self, new_appearance_mode: str\) -> None:\n.*?(?=\n    def _build_sidebar)',
    style_code,
    content,
    flags=re.DOTALL
)

content = content.replace(
    "fig.patch.set_facecolor('#ffffff') # Đồng bộ nền trắng",
    "fig.patch.set_facecolor('#ffffff' if ctk.get_appearance_mode() == 'Light' else '#2b2b2b')\n        ax.set_facecolor('#ffffff' if ctk.get_appearance_mode() == 'Light' else '#2b2b2b')"
)
content = content.replace(
    'ax.set_title("Tỉ lệ xếp loại học lực", fontdict={"fontname": "Segoe UI", "fontsize": 12, "weight": "bold", "color": "#0f172a"})',
    'ax.set_title("Tỉ lệ xếp loại học lực", fontdict={"fontname": "Segoe UI", "fontsize": 12, "weight": "bold", "color": "#0f172a" if ctk.get_appearance_mode() == "Light" else "#f8fafc"})'
)
content = content.replace(
    'fig.patch.set_facecolor(\'#ffffff\')',
    'fig.patch.set_facecolor(\'#ffffff\' if ctk.get_appearance_mode() == \'Light\' else \'#2b2b2b\')\n        ax.set_facecolor(\'#ffffff\' if ctk.get_appearance_mode() == \'Light\' else \'#2b2b2b\')'
)
content = content.replace(
    'fig.suptitle(\'TỈ LỆ PHẦN TRĂM XẾP LOẠI HỌC LỰC\', fontsize=13, fontweight=\'bold\', y=0.95, color="#0f172a")',
    'fig.suptitle(\'TỈ LỆ PHẦN TRĂM XẾP LOẠI HỌC LỰC\', fontsize=13, fontweight=\'bold\', y=0.95, color="#0f172a" if ctk.get_appearance_mode() == "Light" else "#f8fafc")'
)

with open('views_tk.py', 'w', encoding='utf-8') as f:
    f.write(content)
