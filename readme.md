# Obsidian YAML Manager

A robust Python utility and GUI application for bulk managing YAML frontmatter (tags and properties) in Obsidian markdown files.

## Features

- **Bulk Add/Remove**: Quickly add or remove tags and properties across multiple files.
- **Mass Removal**: Integrated support for clearing all tags or all properties from target files.
- **Recursive Processing**: Option to traverse subdirectories for vault-wide updates.
- **Safety First**: Includes a "Dry Run" mode to preview changes and automatic "Backups" before execution.
- **Clean & Organize**: Automatically title-cases, deduplicates, and alphabetizes your frontmatter.
- **Format Preservation**: Powered by `ruamel.yaml` to ensure your markdown comments and formatting remain intact.
- **GUI & CLI**: User-friendly graphical interface or powerful command-line script.

## Getting Started

### Installation

1. Ensure you have Python or Conda installed.
2. Create and activate the environment using the provided `environment.yml`:
   ```bash
   conda env create -f environment.yml
   conda activate obsidian-yaml
   ```

### Running the GUI

The easiest way to work with the manager is via the GUI:
```bash
python gui.py
```
From the GUI, you can browse for folders, select actions, toggle safety flags, and execute the manager with a single click.

### Running via CLI

You can also run the script directly from the command line after adjusting `config.py`:
```bash
python main.py
```

## ⚙️ Configuration (`config.py`)

The behavior of the script is controlled by these parameters. They are mirrored in the GUI application for easy access.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `OBSIDIAN_ROOT` | `Path` | The absolute base directory of your Obsidian vault. |
| `TARGET_DIR` | `Path` | The folder to process (relative to `OBSIDIAN_ROOT` or absolute). |
| `OPERATION` | `String` | Use `"add"`, `"remove"`, or `"clean"`. |
| `TAG` | `String` | The specific tag to add or remove (optional). |
| `PROPERTY` | `Tuple` | The property to target as `("key", "value")` (optional). |
| `RECURSIVE` | `Bool` | Whether to process all subdirectories. |
| `DRY_RUN` | `Bool` | If `True`, shows planned changes in logs without modifying files. |
| `BACKUP` | `Bool` | If `True`, creates a backup of files before modification. |
| `BACKUP_DIR` | `String` | Directory name for stored backups. |
| `LOG_DIR` | `String` | Directory name for operation logs. |
| `REMOVE_ALL_TAGS` | `Bool` | If `True`, logic will wipe all tags from target files. |
| `REMOVE_ALL_PROPERTIES` | `Bool` | If `True`, logic will wipe all properties (excluding aliases/tags) from target files. |

## 🛠️ Development

- **Tests**: Run unit tests using `pytest` from the root directory.
- **Logs**: Operation logs are stored in the `/Logs` folder to keep track of every change.
- **Backups**: If enabled, original files are safely mirrored in the `/Backups` directory.
