import sys
from pathlib import Path
import re
from typing import NamedTuple, Any

file = sys.argv[-1]
file = "tests/SimInfo.h" 
text = Path(file).read_text()

function_pattern = re.compile(r'res\.Get(Integer|Float|Boolean)?\(("?[a-zA-Z0-9_]+"?)\s*,\s*("?[a-zA-Z0-9_]+"?)\s?,\s*("?[a-zA-Z0-9./-]+"?)')
function_matches = function_pattern.finditer(text)
map_pattern = r"std::map\<std::string\s*,\s*[a-zA-Z0-9_-]+\>\s*([a-zA-Z0-9_]+)\s*{\s*"
intern_map = r'(\{"[a-zA-Z0-9_-]+"\s*,\s*[a-zA-Z0-9_-]+\s*}\s*,?\s*)+'
map_pattern += intern_map
pattern = re.compile(map_pattern)
maps_matches = pattern.finditer(text)

TYPES = {
    "Integer": int,
    "Float": float,
    "Boolean": bool,
    None: str,
}

class Argument(NamedTuple):
    """Argument for the Get function"""
    section: str
    parameter: str
    value: Any
    # dtype: Any | list[str] = None


class Map(NamedTuple):
    """Map defining a selection of options"""
    name: str
    options: list[str]

sections = {}
for args in function_matches:
    dtype = TYPES[args.group(1)]
    val = args.group(4)
    if args.group(1) == "Float" and "/" in val:
        val = eval(val)
    val = dtype(val)
    item = Argument(
        section=args.group(2),
        parameter=args.group(3),
        value=val
    )
    print(item)

for mapp in maps_matches:
    key_pattern = r'"([a-zA-Z0-9_-]+\s*)"'
    pattern = re.compile(key_pattern, re.DOTALL)
    intern_map_matches = pattern.findall(mapp.group(0))
    print(mapp.group(1), intern_map_matches)