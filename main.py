import os
from pathlib import Path
import config
from utils import setup_logger, backup_file
from yaml_manager import process_frontmatter

def main():
    logger = setup_logger(config.LOG_DIR)
    
    target_path = config.TARGET_DIR
    if not target_path.is_absolute():
        target_path = config.OBSIDIAN_ROOT / target_path

    logger.info("=========================================")
    logger.info("Starting Obsidian YAML Manager")
    logger.info("=========================================")
    logger.info(f"Target Directory: {target_path}")
    logger.info(f"Operation: {config.OPERATION}")
    logger.info(f"Tag: {config.TAG}")
    logger.info(f"Property: {config.PROPERTY}")
    logger.info(f"Recursive: {config.RECURSIVE}")
    logger.info(f"Dry Run: {config.DRY_RUN}")
    logger.info(f"Backup: {config.BACKUP}")
    logger.info("=========================================")
    
    if not target_path.exists() or not target_path.is_dir():
        logger.error(f"Target directory does not exist or is not a directory: {target_path}")
        return
        
    if config.RECURSIVE:
        md_files = list(target_path.rglob("*.md"))
    else:
        md_files = list(target_path.glob("*.md"))
        
    logger.info(f"Found {len(md_files)} markdown files to process.")
    
    stats = {
        "processed": 0,
        "modified": 0,
        "skipped": 0,
        "errors": 0
    }
    
    for filepath in md_files:
        filepath_str = str(filepath)
        stats["processed"] += 1
        
        try:
            with open(filepath_str, 'r', encoding='utf-8') as f:
                content = f.read()
                
            new_content = process_frontmatter(
                content,
                operation=config.OPERATION,
                tag=config.TAG,
                property_pair=config.PROPERTY
            )
            
            if content != new_content:
                if config.DRY_RUN:
                    logger.info(f"[DRY RUN] Would modify: {filepath_str}")
                    stats["modified"] += 1
                else:
                    if config.BACKUP:
                        success, backup_path = backup_file(filepath_str, str(target_path), config.BACKUP_DIR)
                        if not success:
                            logger.error(f"Failed to backup {filepath_str}: {backup_path}")
                            stats["errors"] += 1
                            continue
                            
                    with open(filepath_str, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                        
                    logger.info(f"Modified: {filepath_str}")
                    stats["modified"] += 1
            else:
                stats["skipped"] += 1
                
        except Exception as e:
            logger.error(f"Error processing {filepath_str}: {str(e)}")
            stats["errors"] += 1
            
    logger.info("=========================================")
    logger.info("Run Summary")
    logger.info(f"Total Files Processed: {stats['processed']}")
    logger.info(f"Files Modified: {stats['modified']}")
    logger.info(f"Files Skipped: {stats['skipped']}")
    logger.info(f"Errors: {stats['errors']}")
    logger.info("=========================================")

if __name__ == "__main__":
    main()
