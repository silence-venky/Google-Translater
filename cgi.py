import re

_parameter_pattern = re.compile(r"\s*;\s*")
_value_pat = re.compile(r"^\s*([^=\s]+)\s*(?:=\s*(.*))?$")


def parse_header(line):
    """Parse a content-type like header.

    Returns the main value and a dict of parameters.
    """
    if line is None:
        return None, {}

    parts = line.split(";")
    main_value = parts[0].strip().lower()
    params = {}

    for item in parts[1:]:
        item = item.strip()
        if not item:
            continue
        if "=" in item:
            name, value = item.split("=", 1)
            name = name.strip().lower()
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
            params[name] = value
        else:
            params[item.lower()] = ""

    return main_value, params
