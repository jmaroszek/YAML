"""
utils.py
Utility functions for logging and file backup operations.
"""

import os
import glob
import shutil
import logging
from datetime import datetime

def setup_logger(log_dir, operation="run", target_folder="", dry_run=False):
    """
    Sets up a logger that creates a new log file for each run
    and keeps only the 5 most recent log files in the directory.
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    # Find existing .log files
    log_file_pattern = os.path.join(log_dir, "*.log")
    log_files = sorted(glob.glob(log_file_pattern), key=os.path.getmtime)
    
    # If we have 5 or more existing log files, remove the oldest until we have 4
    # so that adding the new one keeps the total at 5
    while len(log_files) >= 5:
        oldest = log_files.pop(0)
        try:
            os.remove(oldest)
        except OSError:
            pass
            
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    parts = []
    if dry_run:
        parts.append("DryRun")
    parts.append(str(operation))
    if target_folder:
        clean_folder = str(target_folder).replace("\\", "_").replace("/", "_").replace(" ", "_")
        parts.append(clean_folder)
    parts.append(timestamp)
    
    log_name = "_".join(parts) + ".log"
    log_file = os.path.join(log_dir, log_name)
    
    logger = logging.getLogger("ObsidianYAML")
    logger.setLevel(logging.INFO)
    
    # Ensure handlers are empty (so we don't multiply logs on multiple module calls)
    logger.handlers = []
    
    # Configure file handler
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setLevel(logging.INFO)
    
    # Configure console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Set formatter
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # Add handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger

def backup_file(filepath, base_dir, backup_dir):
    """
    Copies a file to the backup directory, preserving its relative 
    directory structure to base_dir.
    """
    try:
        rel_path = os.path.relpath(filepath, base_dir)
        backup_path = os.path.join(backup_dir, rel_path)
        
        # Ensure the subdirectories exist
        target_dir = os.path.dirname(backup_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
            
        shutil.copy2(filepath, backup_path)
        return True, backup_path
    except Exception as e:
        return False, str(e)
