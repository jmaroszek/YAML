# Obsidian YAML Manager Configuration

This repository contains a script for managing YAML frontmatter in Obsidian markdown files. The behavior of the script is configured using parameters defined in `config.py`.

## Parameters Explained

* **`OBSIDIAN_ROOT`**: (Path object) The base directory for your Obsidian vault. This specifies the root location for resolving relative paths.
* **`TARGET_DIR`**: (Path object) The directory containing the markdown files to process. This can be an absolute path or a path relative to `OBSIDIAN_ROOT`.
* **`OPERATION`**: (String) The kind of change you wish to apply to the frontmatter. Valid options are `"add"` or `"remove"`.
* **`TAG`**: (String or None) The tag string to add or remove from the files in `TARGET_DIR`. Can be set to `None` if you only want to operate on a property.
* **`PROPERTY`**: (Tuple or None) The property to add or remove, defined as a key-value tuple. Example: `("property", "value")`. Set to `None` if you only want to operate on a tag.
* **`RECURSIVE`**: (Boolean) When set to `True`, the script will search for and process markdown files in all subdirectories of `TARGET_DIR` recursively.
* **`DRY_RUN`**: (Boolean) A safety mechanism. If `True`, the script will merely print out and log the intended changes but will *not* actually modify any files.
* **`BACKUP`**: (Boolean) When `True`, the script will create copies of the original markdown files in the folder specified by `BACKUP_DIR` before modifying them.
* **`BACKUP_DIR`**: (String) The path to the folder where backups will be stored (used if `BACKUP` is `True`).
* **`LOG_DIR`**: (String) The path to the folder where operation logs are saved.
