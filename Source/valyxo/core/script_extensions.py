"""ValyxoScript Enhanced Extensions v0.6.0

Additional language features for ValyxoScript:
- Arrays with indexing and methods
- Objects/dictionaries
- Import system for packages
- More built-in functions
- Better string operations
- Lambda expressions
"""

import re
import math
import random
import json
from typing import Any, Dict, List, Optional, Callable, Tuple


class ValyxoArray:
    """Enhanced array type for ValyxoScript."""
    
    def __init__(self, items: List[Any] = None):
        self.items = items or []
    
    def __len__(self):
        return len(self.items)
    
    def __getitem__(self, index):
        if isinstance(index, slice):
            return ValyxoArray(self.items[index])
        return self.items[index]
    
    def __setitem__(self, index, value):
        self.items[index] = value
    
    def __repr__(self):
        return f"[{', '.join(str(x) for x in self.items)}]"
    
    def __iter__(self):
        return iter(self.items)
    
    def push(self, item):
        """Add item to end."""
        self.items.append(item)
        return len(self.items)
    
    def pop(self):
        """Remove and return last item."""
        return self.items.pop() if self.items else None
    
    def shift(self):
        """Remove and return first item."""
        return self.items.pop(0) if self.items else None
    
    def unshift(self, item):
        """Add item to beginning."""
        self.items.insert(0, item)
        return len(self.items)
    
    def slice(self, start, end=None):
        """Return a slice of the array."""
        if end is None:
            return ValyxoArray(self.items[start:])
        return ValyxoArray(self.items[start:end])
    
    def join(self, separator=" "):
        """Join items with separator."""
        return separator.join(str(x) for x in self.items)
    
    def reverse(self):
        """Reverse in place and return."""
        self.items.reverse()
        return self
    
    def sort(self):
        """Sort in place and return."""
        self.items.sort()
        return self
    
    def includes(self, item):
        """Check if item exists."""
        return item in self.items
    
    def index_of(self, item):
        """Find index of item, -1 if not found."""
        try:
            return self.items.index(item)
        except ValueError:
            return -1
    
    def filter(self, predicate: Callable):
        """Filter items by predicate."""
        return ValyxoArray([x for x in self.items if predicate(x)])
    
    def map(self, transform: Callable):
        """Transform each item."""
        return ValyxoArray([transform(x) for x in self.items])
    
    def reduce(self, reducer: Callable, initial=None):
        """Reduce array to single value."""
        result = initial
        for item in self.items:
            if result is None:
                result = item
            else:
                result = reducer(result, item)
        return result
    
    def find(self, predicate: Callable):
        """Find first item matching predicate."""
        for item in self.items:
            if predicate(item):
                return item
        return None


class ValyxoObject:
    """Enhanced object/dictionary type for ValyxoScript."""
    
    def __init__(self, data: Dict[str, Any] = None):
        self._data = data or {}
    
    def __getattr__(self, name):
        if name.startswith('_'):
            return super().__getattribute__(name)
        return self._data.get(name)
    
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self._data[name] = value
    
    def __getitem__(self, key):
        return self._data.get(key)
    
    def __setitem__(self, key, value):
        self._data[key] = value
    
    def __repr__(self):
        pairs = [f"{k}: {repr(v)}" for k, v in self._data.items()]
        return "{" + ", ".join(pairs) + "}"
    
    def __iter__(self):
        return iter(self._data.items())
    
    def keys(self):
        """Get all keys."""
        return ValyxoArray(list(self._data.keys()))
    
    def values(self):
        """Get all values."""
        return ValyxoArray(list(self._data.values()))
    
    def items(self):
        """Get key-value pairs."""
        return ValyxoArray([ValyxoArray([k, v]) for k, v in self._data.items()])
    
    def has(self, key):
        """Check if key exists."""
        return key in self._data
    
    def get(self, key, default=None):
        """Get value with default."""
        return self._data.get(key, default)
    
    def set(self, key, value):
        """Set a value."""
        self._data[key] = value
        return self
    
    def delete(self, key):
        """Delete a key."""
        if key in self._data:
            del self._data[key]
            return True
        return False
    
    def merge(self, other):
        """Merge with another object."""
        if isinstance(other, ValyxoObject):
            self._data.update(other._data)
        elif isinstance(other, dict):
            self._data.update(other)
        return self
    
    def to_dict(self):
        """Convert to plain dict."""
        return self._data.copy()


# Built-in functions for ValyxoScript
BUILTIN_FUNCTIONS: Dict[str, Callable] = {
    # Math functions
    "abs": abs,
    "min": min,
    "max": max,
    "round": round,
    "floor": math.floor,
    "ceil": math.ceil,
    "sqrt": math.sqrt,
    "pow": pow,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "pi": lambda: math.pi,
    "e": lambda: math.e,
    
    # Random functions
    "random": random.random,
    "randint": random.randint,
    "choice": random.choice,
    "shuffle": lambda arr: (random.shuffle(arr.items if isinstance(arr, ValyxoArray) else arr), arr)[1],
    
    # String functions
    "upper": lambda s: s.upper(),
    "lower": lambda s: s.lower(),
    "strip": lambda s: s.strip(),
    "split": lambda s, sep=" ": ValyxoArray(s.split(sep)),
    "replace": lambda s, old, new: s.replace(old, new),
    "startswith": lambda s, p: s.startswith(p),
    "endswith": lambda s, p: s.endswith(p),
    "contains": lambda s, sub: sub in s,
    "substr": lambda s, start, end=None: s[start:end] if end else s[start:],
    "char_at": lambda s, i: s[i] if 0 <= i < len(s) else "",
    "pad_left": lambda s, n, c=" ": s.rjust(n, c),
    "pad_right": lambda s, n, c=" ": s.ljust(n, c),
    "repeat": lambda s, n: s * n,
    "reverse_str": lambda s: s[::-1],
    
    # Type functions
    "type": lambda x: type(x).__name__,
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "is_number": lambda x: isinstance(x, (int, float)),
    "is_string": lambda x: isinstance(x, str),
    "is_array": lambda x: isinstance(x, (list, ValyxoArray)),
    "is_object": lambda x: isinstance(x, (dict, ValyxoObject)),
    
    # Array functions
    "array": lambda *args: ValyxoArray(list(args)),
    "range": lambda start, end, step=1: ValyxoArray(list(range(start, end + 1, step))),
    "len": lambda x: len(x),
    "sum": lambda arr: sum(arr.items if isinstance(arr, ValyxoArray) else arr),
    "avg": lambda arr: sum(arr.items if isinstance(arr, ValyxoArray) else arr) / len(arr),
    "first": lambda arr: (arr.items if isinstance(arr, ValyxoArray) else arr)[0] if arr else None,
    "last": lambda arr: (arr.items if isinstance(arr, ValyxoArray) else arr)[-1] if arr else None,
    "unique": lambda arr: ValyxoArray(list(set(arr.items if isinstance(arr, ValyxoArray) else arr))),
    "flatten": lambda arr: ValyxoArray([item for sublist in arr for item in (sublist.items if isinstance(sublist, ValyxoArray) else [sublist])]),
    "zip": lambda *arrs: ValyxoArray([ValyxoArray(list(x)) for x in zip(*[a.items if isinstance(a, ValyxoArray) else a for a in arrs])]),
    
    # Object functions
    "object": lambda **kwargs: ValyxoObject(kwargs),
    "keys": lambda obj: obj.keys() if hasattr(obj, 'keys') else ValyxoArray(list(obj.keys())),
    "values": lambda obj: obj.values() if hasattr(obj, 'values') else ValyxoArray(list(obj.values())),
    
    # JSON functions
    "json_parse": lambda s: json.loads(s),
    "json_stringify": lambda obj: json.dumps(obj._data if isinstance(obj, ValyxoObject) else obj.items if isinstance(obj, ValyxoArray) else obj),
    
    # Date/Time (simplified)
    "now": lambda: __import__('time').time(),
    "date": lambda: __import__('datetime').datetime.now().isoformat(),
    
    # I/O functions
    "input": lambda prompt="": input(prompt),
    "print_inline": lambda *args: print(*args, end=""),
}


class ValyxoScriptExtensions:
    """Extensions for the ValyxoScript runtime."""
    
    def __init__(self, runtime):
        self.runtime = runtime
        self.imports: Dict[str, Dict[str, Any]] = {}
        self.constants: Dict[str, Any] = {
            "PI": math.pi,
            "E": math.e,
            "TAU": math.tau,
            "INFINITY": float('inf'),
            "NAN": float('nan'),
            "TRUE": True,
            "FALSE": False,
            "NULL": None,
        }
    
    def extend_runtime(self):
        """Add extensions to the runtime."""
        # Add constants
        self.runtime.vars.update(self.constants)
        
        # Add built-in functions to runtime
        for name, func in BUILTIN_FUNCTIONS.items():
            self.runtime.functions[name] = {
                'builtin': True,
                'callable': func
            }
    
    def parse_array_literal(self, expr: str) -> Optional[ValyxoArray]:
        """Parse array literal syntax: [1, 2, 3]"""
        expr = expr.strip()
        if not (expr.startswith('[') and expr.endswith(']')):
            return None
        
        try:
            inner = expr[1:-1].strip()
            if not inner:
                return ValyxoArray()
            
            items = []
            for item in self._split_respecting_brackets(inner, ','):
                item = item.strip()
                if item.startswith('['):
                    items.append(self.parse_array_literal(item))
                elif item.startswith('{'):
                    items.append(self.parse_object_literal(item))
                elif item.startswith('"') or item.startswith("'"):
                    items.append(item[1:-1])
                elif item.lower() in ('true', 'false'):
                    items.append(item.lower() == 'true')
                elif item.lower() == 'null':
                    items.append(None)
                else:
                    try:
                        items.append(int(item))
                    except ValueError:
                        try:
                            items.append(float(item))
                        except ValueError:
                            # Try as variable
                            if item in self.runtime.vars:
                                items.append(self.runtime.vars[item])
                            else:
                                items.append(item)
            
            return ValyxoArray(items)
        except:
            return None
    
    def parse_object_literal(self, expr: str) -> Optional[ValyxoObject]:
        """Parse object literal syntax: {key: value}"""
        expr = expr.strip()
        if not (expr.startswith('{') and expr.endswith('}')):
            return None
        
        try:
            inner = expr[1:-1].strip()
            if not inner:
                return ValyxoObject()
            
            data = {}
            for pair in self._split_respecting_brackets(inner, ','):
                pair = pair.strip()
                if ':' not in pair:
                    continue
                
                key, value = pair.split(':', 1)
                key = key.strip().strip('"\'')
                value = value.strip()
                
                if value.startswith('['):
                    data[key] = self.parse_array_literal(value)
                elif value.startswith('{'):
                    data[key] = self.parse_object_literal(value)
                elif value.startswith('"') or value.startswith("'"):
                    data[key] = value[1:-1]
                elif value.lower() in ('true', 'false'):
                    data[key] = value.lower() == 'true'
                elif value.lower() == 'null':
                    data[key] = None
                else:
                    try:
                        data[key] = int(value)
                    except ValueError:
                        try:
                            data[key] = float(value)
                        except ValueError:
                            if value in self.runtime.vars:
                                data[key] = self.runtime.vars[value]
                            else:
                                data[key] = value
            
            return ValyxoObject(data)
        except:
            return None
    
    def _split_respecting_brackets(self, s: str, delimiter: str) -> List[str]:
        """Split string by delimiter, respecting nested brackets."""
        result = []
        current = []
        depth = 0
        
        for char in s:
            if char in '[{(':
                depth += 1
            elif char in ']})':
                depth -= 1
            
            if char == delimiter and depth == 0:
                result.append(''.join(current))
                current = []
            else:
                current.append(char)
        
        if current:
            result.append(''.join(current))
        
        return result
    
    def handle_import(self, line: str) -> bool:
        """Handle import statement.
        
        Syntax:
            import math
            import math as m
            from math import sin, cos
        """
        # import <package>
        match = re.match(r'import\s+(\w+)(?:\s+as\s+(\w+))?', line)
        if match:
            package, alias = match.groups()
            return self._import_package(package, alias)
        
        # from <package> import <items>
        match = re.match(r'from\s+(\w+)\s+import\s+(.*)', line)
        if match:
            package, items = match.groups()
            return self._import_from(package, items)
        
        return False
    
    def _import_package(self, package: str, alias: str = None) -> bool:
        """Import an entire package."""
        # Import from packages manager if available
        try:
            from .packages import ValyxoPackageManager
            pkg_manager = ValyxoPackageManager()
            pkg = pkg_manager.get_package(package)
            
            if pkg:
                name = alias or package
                self.imports[name] = pkg
                # Add package functions to namespace
                for func_name, func in pkg.items():
                    if callable(func):
                        self.runtime.functions[f"{name}.{func_name}"] = {
                            'builtin': True,
                            'callable': func
                        }
                return True
        except ImportError:
            pass
        
        return False
    
    def _import_from(self, package: str, items_str: str) -> bool:
        """Import specific items from a package."""
        items = [i.strip() for i in items_str.split(',')]
        
        try:
            from .packages import ValyxoPackageManager
            pkg_manager = ValyxoPackageManager()
            pkg = pkg_manager.get_package(package)
            
            if pkg:
                for item in items:
                    if item in pkg:
                        self.runtime.functions[item] = {
                            'builtin': True,
                            'callable': pkg[item]
                        }
                return True
        except ImportError:
            pass
        
        return False
    
    def handle_const(self, line: str) -> bool:
        """Handle const declaration.
        
        Syntax: const NAME = value
        """
        match = re.match(r'const\s+(\w+)\s*=\s*(.*)', line)
        if not match:
            return False
        
        name, value_expr = match.groups()
        try:
            value = self.runtime.safe_eval(value_expr)
            self.constants[name] = value
            self.runtime.vars[name] = value
            return True
        except:
            return False
    
    def handle_array_method(self, line: str) -> Tuple[bool, Any]:
        """Handle array method calls.
        
        Syntax: arr.push(item), arr.pop(), etc.
        """
        match = re.match(r'(\w+)\.(\w+)\((.*?)\)', line)
        if not match:
            return False, None
        
        var_name, method_name, args_str = match.groups()
        
        if var_name not in self.runtime.vars:
            return False, None
        
        obj = self.runtime.vars[var_name]
        
        if not hasattr(obj, method_name):
            return False, None
        
        method = getattr(obj, method_name)
        
        if not callable(method):
            return True, method  # It's a property
        
        # Parse arguments
        args = []
        if args_str.strip():
            for arg in self._split_respecting_brackets(args_str, ','):
                arg = arg.strip()
                try:
                    args.append(self.runtime.safe_eval(arg))
                except:
                    args.append(arg)
        
        result = method(*args)
        return True, result
    
    def handle_index_access(self, line: str) -> Tuple[bool, Any]:
        """Handle array/object index access.
        
        Syntax: arr[0], obj["key"], arr[1:3]
        """
        match = re.match(r'(\w+)\[(.*?)\](?:\s*=\s*(.*))?', line)
        if not match:
            return False, None
        
        var_name, index_expr, value_expr = match.groups()
        
        if var_name not in self.runtime.vars:
            return False, None
        
        obj = self.runtime.vars[var_name]
        
        try:
            # Parse index
            index = self.runtime.safe_eval(index_expr)
            
            if value_expr is not None:
                # Assignment
                value = self.runtime.safe_eval(value_expr)
                obj[index] = value
                return True, value
            else:
                # Access
                return True, obj[index]
        except Exception as e:
            return False, None
    
    def handle_spread(self, expr: str) -> Optional[List[Any]]:
        """Handle spread operator: ...arr"""
        match = re.match(r'\.\.\.(\w+)', expr)
        if not match:
            return None
        
        var_name = match.group(1)
        if var_name not in self.runtime.vars:
            return None
        
        obj = self.runtime.vars[var_name]
        if isinstance(obj, ValyxoArray):
            return obj.items
        elif isinstance(obj, (list, tuple)):
            return list(obj)
        return None
    
    def handle_destructuring(self, line: str) -> bool:
        """Handle destructuring assignment.
        
        Syntax: 
            set [a, b, c] = arr
            set {x, y} = obj
        """
        # Array destructuring
        match = re.match(r'set\s+\[(.*?)\]\s*=\s*(\w+)', line)
        if match:
            vars_str, source = match.groups()
            if source not in self.runtime.vars:
                return False
            
            source_val = self.runtime.vars[source]
            items = source_val.items if isinstance(source_val, ValyxoArray) else list(source_val)
            
            var_names = [v.strip() for v in vars_str.split(',')]
            for i, var_name in enumerate(var_names):
                if var_name:
                    self.runtime.vars[var_name] = items[i] if i < len(items) else None
            return True
        
        # Object destructuring
        match = re.match(r'set\s+\{(.*?)\}\s*=\s*(\w+)', line)
        if match:
            vars_str, source = match.groups()
            if source not in self.runtime.vars:
                return False
            
            source_val = self.runtime.vars[source]
            if isinstance(source_val, ValyxoObject):
                data = source_val._data
            elif isinstance(source_val, dict):
                data = source_val
            else:
                return False
            
            var_names = [v.strip() for v in vars_str.split(',')]
            for var_name in var_names:
                if var_name:
                    self.runtime.vars[var_name] = data.get(var_name)
            return True
        
        return False
    
    def handle_for_each(self, line: str) -> Optional[Dict[str, Any]]:
        """Handle for-each loop.
        
        Syntax: for item in array {
        """
        match = re.match(r'for\s+(\w+)\s+in\s+(\w+)\s*{', line)
        if not match:
            return None
        
        var_name, iterable_name = match.groups()
        
        if iterable_name not in self.runtime.vars:
            return None
        
        iterable = self.runtime.vars[iterable_name]
        if isinstance(iterable, ValyxoArray):
            items = iterable.items
        elif isinstance(iterable, (list, tuple)):
            items = list(iterable)
        elif isinstance(iterable, (ValyxoObject, dict)):
            items = list(iterable.items() if isinstance(iterable, dict) else iterable._data.items())
        else:
            return None
        
        return {
            'type': 'for_each',
            'var': var_name,
            'items': items,
            'lines': []
        }


def integrate_extensions(runtime):
    """Integrate extensions into a ValyxoScript runtime."""
    ext = ValyxoScriptExtensions(runtime)
    ext.extend_runtime()
    return ext
