import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import backup_file

def test_backup_file(tmp_path):
    base_dir = tmp_path / "base"
    base_dir.mkdir()
    
    backup_dir = tmp_path / "backup"
    backup_dir.mkdir()
    
    sub_dir = base_dir / "subdir"
    sub_dir.mkdir()
    
    test_file = sub_dir / "test.md"
    test_file.write_text("hello", encoding="utf-8")
    
    success, b_path = backup_file(str(test_file), str(base_dir), str(backup_dir))
    
    assert success
    assert os.path.exists(b_path)
    with open(b_path, encoding="utf-8") as f:
        assert f.read() == "hello"
    assert "subdir" in b_path
