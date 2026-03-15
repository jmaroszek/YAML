import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
import os
from pathlib import Path

# Assuming gui.py is in the same directory as config.py
CONFIG_FILE = Path(__file__).parent / "config.py"

def load_config():
    config = {}
    if not CONFIG_FILE.exists():
        return config
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse using regex
    m = re.search(r'OBSIDIAN_ROOT\s*=\s*Path\((["\'])(.*?)\1\)', content)
    config['OBSIDIAN_ROOT'] = m.group(2) if m else "Root"

    m = re.search(r'TARGET_DIR\s*=\s*Path\((["\'])(.*?)\1\)', content)
    config['TARGET_DIR'] = m.group(2) if m else "Folder"

    m = re.search(r'OPERATION\s*=\s*(["\'])(.*?)\1', content)
    config['OPERATION'] = m.group(2) if m else "add"

    m = re.search(r'TAG\s*=\s*(None|["\'].*?["\'])', content)
    tag_val = m.group(1) if m else "None"
    config['TAG'] = "" if tag_val == "None" else tag_val.strip("\"'")

    m = re.search(r'PROPERTY\s*=\s*(None|\(.*?\)|["\'].*?["\'])', content)
    prop_val = m.group(1) if m else "None"
    config['PROPERTY_KEY'] = ""
    config['PROPERTY_VALUE'] = ""
    if prop_val != "None":
        try:
            import ast
            parts = ast.literal_eval(prop_val)
            if isinstance(parts, tuple) and len(parts) == 2:
                config['PROPERTY_KEY'] = str(parts[0])
                config['PROPERTY_VALUE'] = str(parts[1])
        except Exception:
            pass

    m = re.search(r'RECURSIVE\s*=\s*(True|False)', content)
    config['RECURSIVE'] = (m.group(1) == "True") if m else False

    m = re.search(r'DRY_RUN\s*=\s*(True|False)', content)
    config['DRY_RUN'] = (m.group(1) == "True") if m else False

    m = re.search(r'BACKUP\s*=\s*(True|False)', content)
    config['BACKUP'] = (m.group(1) == "True") if m else False

    m = re.search(r'BACKUP_DIR\s*=\s*(["\'])(.*?)\1', content)
    config['BACKUP_DIR'] = m.group(2) if m else "Backups"

    m = re.search(r'LOG_DIR\s*=\s*(["\'])(.*?)\1', content)
    config['LOG_DIR'] = m.group(2) if m else "Logs"

    m = re.search(r'REMOVE_ALL_TAGS\s*=\s*(True|False)', content)
    config['REMOVE_ALL_TAGS'] = (m.group(1) == "True") if m else False

    m = re.search(r'REMOVE_ALL_PROPERTIES\s*=\s*(True|False)', content)
    config['REMOVE_ALL_PROPERTIES'] = (m.group(1) == "True") if m else False

    return config

def save_config(config):
    if not CONFIG_FILE.exists():
        messagebox.showerror("Error", f"{CONFIG_FILE.name} not found in {CONFIG_FILE.parent}!")
        return

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Helpers for regex replacements
    def replace_path(var_name, val, text):
        return re.sub(
            rf'^({var_name}\s*=\s*Path\()(["\']).*?\2(\).*)$',
            rf'\g<1>"{val}"\g<3>',
            text, flags=re.MULTILINE
        )

    def replace_str(var_name, val, text):
        return re.sub(
            rf'^({var_name}\s*=\s*)(["\']).*?\2(.*)$',
            rf'\g<1>"{val}"\g<3>',
            text, flags=re.MULTILINE
        )

    def replace_str_or_none(var_name, val, text):
        new_val = f'"{val}"' if val else "None"
        return re.sub(
            rf'^({var_name}\s*=\s*)(?:None|["\'].*?["\'])(.*)$',
            rf'\g<1>{new_val}\g<2>',
            text, flags=re.MULTILINE
        )

    def replace_tuple_or_none(var_name, key, val, text):
        new_val = f'("{key}", "{val}")' if key else "None"
        return re.sub(
            rf'^({var_name}\s*=\s*)(?:None|\(.*?\)|["\'].*?["\'])(.*)$',
            rf'\g<1>{new_val}\g<2>',
            text, flags=re.MULTILINE
        )

    def replace_bool(var_name, val, text):
        new_val = "True" if val else "False"
        return re.sub(
            rf'^({var_name}\s*=\s*)(?:True|False)(.*)$',
            rf'\g<1>{new_val}\g<2>',
            text, flags=re.MULTILINE
        )

    # Perform updates
    content = replace_path('OBSIDIAN_ROOT', config['OBSIDIAN_ROOT'], content)
    content = replace_path('TARGET_DIR', config['TARGET_DIR'], content)
    content = replace_str('OPERATION', config['OPERATION'], content)
    content = replace_str_or_none('TAG', config['TAG'], content)
    content = replace_tuple_or_none('PROPERTY', config['PROPERTY_KEY'], config['PROPERTY_VALUE'], content)
    content = replace_bool('RECURSIVE', config['RECURSIVE'], content)
    content = replace_bool('DRY_RUN', config['DRY_RUN'], content)
    content = replace_bool('BACKUP', config['BACKUP'], content)
    content = replace_str('BACKUP_DIR', config['BACKUP_DIR'], content)
    content = replace_str('LOG_DIR', config['LOG_DIR'], content)
    content = replace_bool('REMOVE_ALL_TAGS', config['REMOVE_ALL_TAGS'], content)
    content = replace_bool('REMOVE_ALL_PROPERTIES', config['REMOVE_ALL_PROPERTIES'], content)

    # Write back
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(content)
class ConfigGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YAML Manager Configuration")
        self.root.resizable(False, False)

        # Style Configuration
        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
        style.configure("TCheckbutton", font=("Segoe UI", 10))

        self.config = load_config()

        # tkinter Double/String Variables
        self.obsidian_root_var = tk.StringVar(value=self.config.get('OBSIDIAN_ROOT', ''))
        self.target_dir_var = tk.StringVar(value=self.config.get('TARGET_DIR', ''))
        self.operation_var = tk.StringVar(value=self.config.get('OPERATION', 'add').title())
        self.tag_var = tk.StringVar(value=self.config.get('TAG', ''))
        self.property_key_var = tk.StringVar(value=self.config.get('PROPERTY_KEY', ''))
        self.property_val_var = tk.StringVar(value=self.config.get('PROPERTY_VALUE', ''))
        self.recursive_var = tk.BooleanVar(value=self.config.get('RECURSIVE', False))
        self.dry_run_var = tk.BooleanVar(value=self.config.get('DRY_RUN', False))
        self.backup_var = tk.BooleanVar(value=self.config.get('BACKUP', False))
        self.remove_all_tags_var = tk.BooleanVar(value=self.config.get('REMOVE_ALL_TAGS', False))
        self.remove_all_props_var = tk.BooleanVar(value=self.config.get('REMOVE_ALL_PROPERTIES', False))
        self.backup_dir_var = tk.StringVar(value=self.config.get('BACKUP_DIR', ''))
        self.log_dir_var = tk.StringVar(value=self.config.get('LOG_DIR', ''))

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        row = 0
        def add_row(label_text, widget, is_checkbox=False, tooltip=None):
            nonlocal row
            lbl = ttk.Label(main_frame, text=label_text)
            lbl.grid(row=row, column=0, sticky='w', pady=8, padx=5)
            
            if not is_checkbox:
                widget.grid(row=row, column=1, sticky='ew', pady=8, padx=5)
            else:
                widget.grid(row=row, column=1, sticky='w', pady=8, padx=5)
            row += 1

        # TARGET_DIR
        target_frame = ttk.Frame(main_frame)
        ttk.Entry(target_frame, textvariable=self.target_dir_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(target_frame, text="Browse", width=8, command=self.browse_target).pack(side=tk.LEFT, padx=(5, 0))
        add_row("Folder:", target_frame)

        # OPERATION
        op_combo = ttk.Combobox(main_frame, textvariable=self.operation_var, 
                                values=["Add", "Remove", "Clean"], state="readonly")
        add_row("Action:", op_combo)

        # TAG
        add_row("Tag:", ttk.Entry(main_frame, textvariable=self.tag_var))

        # PROPERTY
        prop_frame = ttk.Frame(main_frame)
        ttk.Entry(prop_frame, textvariable=self.property_key_var, width=15).pack(side=tk.LEFT)
        ttk.Label(prop_frame, text="Value:").pack(side=tk.LEFT, padx=(10, 5))
        ttk.Entry(prop_frame, textvariable=self.property_val_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        add_row("Property:", prop_frame)

        # FLAGS
        flags_frame = ttk.Frame(main_frame)
        ttk.Checkbutton(flags_frame, text="Recursive", variable=self.recursive_var).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Checkbutton(flags_frame, text="Dry Run", variable=self.dry_run_var).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Checkbutton(flags_frame, text="Backup", variable=self.backup_var).pack(side=tk.LEFT, padx=(0, 15))
        flags_frame.grid(row=row, column=0, columnspan=2, pady=(15, 5), sticky='w', padx=5) 
        row += 1

        # MASS REMOVAL
        mass_frame = ttk.Frame(main_frame)
        ttk.Checkbutton(mass_frame, text="Remove all tags", variable=self.remove_all_tags_var).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Checkbutton(mass_frame, text="Remove all properties", variable=self.remove_all_props_var).pack(side=tk.LEFT, padx=(0, 15))
        mass_frame.grid(row=row, column=0, columnspan=2, pady=(0, 15), sticky='w', padx=5)
        row += 1

        main_frame.columnconfigure(1, weight=1)

        # Action Buttons Frame
        btn_frame = ttk.Frame(self.root, padding="15")
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(btn_frame, text="", foreground="#007ACC")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Save and Run gets side=tk.RIGHT first so it's most prominent on right, Save Only gets side=tk.RIGHT next so it's to its left
        ttk.Button(btn_frame, text="Save and Run", command=self.run_main, width=20).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Save Only", command=self.save, width=15).pack(side=tk.RIGHT, padx=5)

    def browse_target(self):
        # Open directory browser
        d = filedialog.askdirectory(initialdir=self.target_dir_var.get(), title="Select Target Directory")
        if d:
            self.target_dir_var.set(d.replace('/', '\\\\'))

    def run_main(self):
        self.save()
        import subprocess
        import sys
        main_script = Path(__file__).parent / "main.py"
        if not main_script.exists():
            messagebox.showerror("Error", f"main.py not found at {main_script}")
            return
        
        try:
            # We use creationflags to run without a separate console window taking focus
            if sys.platform == "win32":
                subprocess.Popen([sys.executable, str(main_script)], 
                                 creationflags=subprocess.CREATE_NO_WINDOW,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            if self.dry_run_var.get():
                self.status_label.config(text=f"Check Logs")
            else:
                self.status_label.config(text="Success!")
            self.root.after(3500, lambda: self.status_label.config(text=""))
        except Exception as e:
            messagebox.showerror("Execution Error", f"Failed to run main.py: {e}")

    def save(self):
        # Prevent completely empty tags where None is more appropriate
        config_to_save = {
            'OBSIDIAN_ROOT': self.obsidian_root_var.get().replace("\\", "\\\\").replace("\\\\\\\\", "\\\\"),  
            'TARGET_DIR': self.target_dir_var.get().replace("\\", "\\\\").replace("\\\\\\\\", "\\\\"),
            'OPERATION': self.operation_var.get().lower(),
            'TAG': self.tag_var.get().strip() or "",
            'PROPERTY_KEY': self.property_key_var.get().strip(),
            'PROPERTY_VALUE': self.property_val_var.get().strip(),
            'RECURSIVE': self.recursive_var.get(),
            'DRY_RUN': self.dry_run_var.get(),
            'BACKUP': self.backup_var.get(),
            'BACKUP_DIR': self.backup_dir_var.get(),
            'LOG_DIR': self.log_dir_var.get(),
            'REMOVE_ALL_TAGS': self.remove_all_tags_var.get(),
            'REMOVE_ALL_PROPERTIES': self.remove_all_props_var.get(),
        }
        # A little fix on the backslash replace: Let's sanitize to ensure single forward slashes OR raw string behavior isn't messed up
        obs_root = self.obsidian_root_var.get()
        # It's cleaner to handle paths without double backslashing string manually if we just format it directly
        config_to_save['OBSIDIAN_ROOT'] = obs_root.replace('\\', '/')
        config_to_save['TARGET_DIR'] = self.target_dir_var.get().replace('\\', '/')
        
        save_config(config_to_save)
        self.status_label.config(text="Configuration Saved!")
        self.root.after(2500, lambda: self.status_label.config(text=""))

if __name__ == "__main__":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
        
    root = tk.Tk()
    app = ConfigGUI(root)
    
    root.update_idletasks()
    
    # Dynamically scale window footprint while enforcing minimums 
    window_width = max(580, root.winfo_reqwidth())
    window_height = max(360, root.winfo_reqheight())
    
    # Center window
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    x = int((screen_width/2) - (window_width/2))
    y = int((screen_height/2) - (window_height/2))
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    root.mainloop()
