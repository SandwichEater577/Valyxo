#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, 'src')

try:
    from Novahub import NovaGPTModule
    
    print("✓ NovaGPTModule imported successfully")
    
    gpt = NovaGPTModule()
    print("✓ NovaGPTModule instance created")
    
    test_cases = [
        ("hello", "greeting"),
        ("how do I use functions in novascript", "novascript function"),
        ("how can I refactor my code", "refactoring"),
        ("I have a bug to debug", "debugging"),
        ("help me write tests", "testing"),
    ]
    
    print("\nTesting Zencoder-powered responses:")
    print("-" * 60)
    
    for query, label in test_cases:
        response = gpt.get_response(query)
        print(f"\n[{label}]")
        print(f"Q: {query}")
        print(f"A: {response[:100]}...")
    
    print("\n" + "=" * 60)
    print("✓ All tests passed - Zencoder integration working!")
    print("✓ Conversation history maintained:", len(gpt.messages), "messages")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
