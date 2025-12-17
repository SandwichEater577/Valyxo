#!/usr/bin/env python3
import sys
import os
import io

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from Valyxo import ValyxoScriptRuntime

def capture_output(func):
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        func()
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    return output

def test_for_loop_prints():
    print("Test: for_loop_prints")
    runtime = ValyxoScriptRuntime()
    
    def run_test():
        runtime.run_line('set sum = 0')
        runtime.run_line('for i in 1 to 3 {')
        runtime.run_line('  print i')
        runtime.run_line('  set sum = sum + i')
        runtime.run_line('}')
    
    output = capture_output(run_test)
    assert '1' in output and '2' in output and '3' in output, f"Expected output to contain 1, 2, 3. Got: {output}"
    assert runtime.vars['sum'] == 6, f"Expected sum=6, got {runtime.vars['sum']}"
    print("  PASS")

def test_while_loop_print():
    print("Test: while_loop_print")
    runtime = ValyxoScriptRuntime()
    
    def run_test():
        runtime.run_line('set i = 1')
        runtime.run_line('while [i <= 3] {')
        runtime.run_line('  print i')
        runtime.run_line('  set i = i + 1')
        runtime.run_line('}')
    
    output = capture_output(run_test)
    assert '1' in output and '2' in output and '3' in output, f"Expected output to contain 1, 2, 3. Got: {output}"
    print("  PASS")

def test_infinite_loop_detection():
    print("Test: infinite_loop_detection")
    runtime = ValyxoScriptRuntime()
    runtime.MAX_ITERATIONS = 10
    runtime.run_line('set i = 1')
    try:
        runtime.run_line('while [True] {')
        runtime.run_line('  set i = i + 1')
        runtime.run_line('}')
        assert False, "Should have raised RuntimeError"
    except RuntimeError:
        pass
    print("  PASS")

def test_function_definition_and_call():
    print("Test: function_definition_and_call")
    runtime = ValyxoScriptRuntime()
    
    def run_test():
        runtime.run_line('func greet(name) {')
        runtime.run_line('  print "Hello " + name')
        runtime.run_line('}')
        runtime.run_line('greet("Test")')
    
    output = capture_output(run_test)
    assert 'Hello Test' in output, f"Expected 'Hello Test', got: {output}"
    print("  PASS")

def test_function_with_return_like_behavior():
    print("Test: function_with_return_like_behavior")
    runtime = ValyxoScriptRuntime()
    
    def run_test():
        runtime.run_line('func add(a, b) {')
        runtime.run_line('  print a + b')
        runtime.run_line('}')
        runtime.run_line('add(3, 4)')
    
    output = capture_output(run_test)
    assert '7' in output, f"Expected '7', got: {output}"
    print("  PASS")

def test_safe_eval_basic():
    print("Test: safe_eval_basic")
    runtime = ValyxoScriptRuntime()
    assert runtime.safe_eval('2 + 3') == 5
    assert runtime.safe_eval('10 - 4') == 6
    assert runtime.safe_eval('2 * 3') == 6
    assert runtime.safe_eval('9 / 3') == 3
    assert runtime.safe_eval('2 ** 3') == 8
    print("  PASS")

def test_set_and_print():
    print("Test: set_and_print")
    runtime = ValyxoScriptRuntime()
    runtime.run_line('set x = 42')
    assert 'x' in runtime.vars
    
    def run_test():
        runtime.run_line('print x')
    
    output = capture_output(run_test)
    assert '42' in output, f"Expected '42', got: {output}"
    print("  PASS")

def test_unknown_variable_raises():
    print("Test: unknown_variable_raises")
    runtime = ValyxoScriptRuntime()
    try:
        runtime.safe_eval('y + 1')
        assert False, "Should have raised RuntimeError"
    except RuntimeError:
        pass
    print("  PASS")

if __name__ == '__main__':
    tests = [
        test_for_loop_prints,
        test_while_loop_print,
        test_infinite_loop_detection,
        test_function_definition_and_call,
        test_function_with_return_like_behavior,
        test_safe_eval_basic,
        test_set_and_print,
        test_unknown_variable_raises,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  FAIL: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print(f"\n{passed} passed, {failed} failed")
    if failed > 0:
        sys.exit(1)
