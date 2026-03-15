"""
yaml_manager.py
Core logic for parsing, modifying, and dumping Obsidian YAML frontmatter.
"""

from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO

def title_case(val):
    """
    Capitalizes the first letter of each word in a string/tag/property value.
    If it's a list, applies title case to all string elements.
    """
    if isinstance(val, str):
        return val.title()
    elif isinstance(val, list):
        return [title_case(v) for v in val]
    return val

def deduplicate_and_sort(lst):
    """
    Deduplicates a list while preserving title case, 
    and sorts it alphabetically.
    """
    if not isinstance(lst, list):
        return lst
    
    unique = []
    seen = set()
    for item in lst:
        if item not in seen:
            seen.add(item)
            unique.append(item)
            
    # Need to handle homogeneous sorting. Usually tags/aliases are strings.
    try:
        unique.sort()
    except TypeError:
        # If heterogeneous, sort by string representation
        unique.sort(key=str)
        
    return unique

def parse_frontmatter_and_body(content):
    """
    Extracts the YAML frontmatter block and the body from markdown content.
    Returns (frontmatter_string, body_string).
    If no frontmatter exists, returns ('', content).
    """
    if content.startswith("---\n"):
        parts = content.split("---\n", 2)
        if len(parts) >= 3:
            return parts[1], parts[2]
            
    if content.startswith("---\r\n"):
        parts = content.split("---\r\n", 2)
        if len(parts) >= 3:
            return parts[1], parts[2]
            
    return "", content

def process_frontmatter(content, operation=None, tag=None, property_pair=None, remove_all_tags=False, remove_all_props=False):
    """
    Reads the full markdown string, modifies frontmatter, and returns the modified string.
    """
    fm_str, body = parse_frontmatter_and_body(content)
    
    yaml = YAML()
    yaml.default_flow_style = False
    yaml.preserve_quotes = True
    yaml.width = 4096  # Prevent wrapping long lines
    
    # Load existing data
    if fm_str.strip():
        data = yaml.load(fm_str)
        if data is None:
            data = {}
    else:
        data = {}
        
    # 1. Standardize dictionary keys to lowercase
    standardized_data = {}
    for k, v in data.items():
        if isinstance(k, str):
            standardized_data[k.lower()] = v
        else:
            standardized_data[k] = v
    data = standardized_data

    # Mass Removals
    if remove_all_tags:
        data.pop('tags', None)
        
    if remove_all_props:
        keys_to_clear = [k for k in data.keys() if k not in ('aliases', 'tags')]
        for k in keys_to_clear:
            data.pop(k, None)

    # 2. Add/Remove Tag
    if tag:
        t_tag = title_case(tag)
        current_tags = data.get('tags', [])
        
        # Normalize to list if string
        if not isinstance(current_tags, list):
            if current_tags:
                current_tags = [current_tags]
            else:
                current_tags = []
                
        # Title case to match accurately
        current_tags = title_case(current_tags)
        
        if operation == 'add':
            if t_tag not in current_tags:
                current_tags.append(t_tag)
        elif operation == 'remove':
            if t_tag in current_tags:
                current_tags.remove(t_tag)
                
        data['tags'] = current_tags

    # 3. Add/Remove Property
    if property_pair:
        prop_key, prop_val = property_pair
        p_key = prop_key.lower()
        t_val = title_case(prop_val)
        
        if operation == 'add':
            existing_val = data.get(p_key)
            if existing_val is None:
                data[p_key] = t_val
            elif isinstance(existing_val, list):
                t_existing = title_case(existing_val)
                if t_val not in t_existing:
                    t_existing.append(t_val)
                data[p_key] = t_existing
            else:
                # convert to list
                t_existing = title_case(existing_val)
                if t_existing != t_val:
                    data[p_key] = [t_existing, t_val]
                else:
                    data[p_key] = t_existing
                    
        elif operation == 'remove':
            existing_val = data.get(p_key)
            if existing_val is not None:
                if not prop_val:
                    data.pop(p_key, None)
                elif isinstance(existing_val, list):
                    t_existing = title_case(existing_val)
                    if t_val in t_existing:
                        t_existing.remove(t_val)
                    data[p_key] = t_existing
                else:
                    if title_case(existing_val) == t_val:
                        data.pop(p_key, None)

    # 4. Clean, title case, deduplicate
    keys_to_remove = []
    
    for k, v in data.items():
        if v is None:
            keys_to_remove.append(k)
            continue
            
        t_val = title_case(v)
        
        if isinstance(t_val, list):
            t_val = deduplicate_and_sort(t_val)
            if not t_val:  # Empty list -> remove entirely
                keys_to_remove.append(k)
            else:
                data[k] = t_val
        else:
            # String or other type
            if t_val == "" or str(t_val).strip() == "":
                keys_to_remove.append(k)
            else:
                data[k] = t_val

    for k in keys_to_remove:
        data.pop(k, None)

    # 5. Reorder keys: aliases, tags, properties (alphabetical)
    final_dict = yaml.map()
    
    if 'aliases' in data:
        final_dict['aliases'] = data['aliases']
        
    if 'tags' in data:
        final_dict['tags'] = data['tags']
        
    other_keys = sorted([k for k in data.keys() if k not in ('aliases', 'tags')])
    for k in other_keys:
        final_dict[k] = data[k]

    # Dump yaml
    if final_dict:
        stream = StringIO()
        yaml.dump(final_dict, stream)
        new_fm_str = stream.getvalue()
        return f"---\n{new_fm_str}---\n{body}"
    else:
        # No frontmatter left, maybe some operations removed everything or it was empty
        # and we strip out the unneeded tags.
        # But maybe preserving body without empty --- --- is safer and cleaner
        return body
