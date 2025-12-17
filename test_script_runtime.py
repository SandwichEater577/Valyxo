#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from Valyxo import ValyxoScriptRuntime

def test_basic():
    print("Test 1: Basic set and variable storage")
    rt = ValyxoScriptRuntime()
    rt.run_line('set x = 42')
    assert rt.vars['x'] == 42, f"Expected 42, got {rt.vars['x']}"
    print("  PASS")

def test_safe_eval():
    print("Test 2: Safe eval expressions")
    rt = ValyxoScriptRuntime()
    assert rt.safe_eval('2 + 3') == 5
    assert rt.safe_eval('10 - 4') == 6
    assert rt.safe_eval('2 * 3') == 6
    print("  PASS")

def test_print(capsule=False):
    print("Test 3: Print command")
    rt = ValyxoScriptRuntime()
    rt.run_line('set msg = "Hello"')
    rt.run_line('print msg')
    assert 'msg' in rt.vars
    print("  PASS")

def test_for_loop():
    print("Test 4: For loop")
    rt = ValyxoScriptRuntime()
    rt.run_line('set sum = 0')
    rt.run_line('for i in 1 to 3 {')
    rt.run_line('  set sum = sum + i')
    rt.run_line('}')
    assert rt.vars['sum'] == 6, f"Expected 6, got {rt.vars['sum']}"
    print("  PASS")

def test_while_loop():
    print("Test 5: While loop")
    rt = ValyxoScriptRuntime()
    rt.run_line('set i = 1')
    rt.run_line('set sum = 0')
    rt.run_line('while [i <= 3] {')
    rt.run_line('  set sum = sum + i')
    rt.run_line('  set i = i + 1')
    rt.run_line('}')
    assert rt.vars['sum'] == 6, f"Expected 6, got {rt.vars['sum']}"
    print("  PASS")

def test_function_def():
    print("Test 6: Function definition and call")
    rt = ValyxoScriptRuntime()
    rt.run_line('func add(a, b) {')
    rt.run_line('  print a + b')
    rt.run_line('}')
    rt.run_line('add(3, 4)')
    assert 'add' in rt.functions
    print("  PASS")

def test_infinite_loop_detection():
    print("Test 7: Infinite loop detection")
    rt = ValyxoScriptRuntime()
    rt.MAX_ITERATIONS = 10
    rt.run_line('set i = 1')
    try:
        rt.run_line('while [True] {')
        rt.run_line('  set i = i + 1')
        rt.run_line('}')
        assert False, "Should have raised RuntimeError"
    except RuntimeError as e:
        assert "iteration limit" in str(e).lower()
        print("  PASS")

if __name__ == '__main__':
    try:
        test_basic()
        test_safe_eval()
        test_print()
        test_for_loop()
        test_while_loop()
        test_function_def()
        test_infinite_loop_detection()
        print("\nAll tests passed!")
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
