import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from yaml_manager import process_frontmatter, title_case, deduplicate_and_sort

def test_title_case():
    assert title_case("status/active") == "Status/Active"
    assert title_case("hello world") == "Hello World"
    assert title_case(["one", "two"]) == ["One", "Two"]

def test_deduplicate_and_sort():
    lst = ["Beta", "Alpha", "Beta", "Gamma"]
    assert deduplicate_and_sort(lst) == ["Alpha", "Beta", "Gamma"]

def test_add_tag_no_frontmatter():
    content = "Just some body text."
    new_content = process_frontmatter(content, operation="add", tag="new tag")
    assert "---\n" in new_content
    assert "tags:" in new_content
    assert "New Tag" in new_content
    assert "Just some body text." in new_content

def test_add_property_existing_frontmatter():
    content = "---\nzeta: value\nalpha: value\n---\nbody"
    new_content = process_frontmatter(content, operation="add", property_pair=("beta", "test value"))
    assert "beta: Test Value" in new_content
    # Check ordering
    assert new_content.index("alpha:") < new_content.index("beta:") < new_content.index("zeta:")

def test_formatting_order():
    content = "---\nzeta: value\ntags: my_tag\naliases: my_alias\n---\nbody"
    new_content = process_frontmatter(content)
    assert new_content.index("aliases:") < new_content.index("tags:") < new_content.index("zeta:")

def test_remove_tag():
    content = "---\ntags:\n  - To Remove\n  - Keep\n---\nbody"
    new_content = process_frontmatter(content, operation="remove", tag="to remove")
    assert "Keep" in new_content
    assert "To Remove" not in new_content

def test_remove_property():
    content = "---\nstatus: active\n---\nbody"
    new_content = process_frontmatter(content, operation="remove", property_pair=("status", "active"))
    assert "status:" not in new_content
    assert "body" in new_content
    
def test_clean_empty_fields():
    content = "---\ntags: []\naliases: \nstatus: \n---\nbody"
    new_content = process_frontmatter(content)
    assert "tags:" not in new_content
    assert "aliases:" not in new_content
    assert "status:" not in new_content
