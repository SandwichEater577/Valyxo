import os
import json
from typing import List, Dict, Optional
from .constants import API_KEY_PATH, CONFIG_DIR


class ValyxoGPTModule:
    """AI Assistant module for Valyxo v0.5.1, powered by Zencoder.
    
    Manages conversation history and provides intelligent responses for
    coding assistance, debugging, and development guidance.
    
    Features:
    - Context-aware responses
    - Multi-turn conversations
    - Specialized categories (coding, ValyxoScript, debugging, etc.)
    - Conversation history management
    """

    MAX_HISTORY = 50
    
    SYSTEM_PROMPTS = {
        "coding": "You are an expert coding assistant. Provide clear, concise solutions with code examples.",
        "valyxoscript": "You are a ValyxoScript expert. Help users with ValyxoScript syntax, functions, and best practices.",
        "debugging": "You are a debugging expert. Help identify and fix code issues with clear explanations.",
        "performance": "You are a performance optimization expert. Provide advice on code efficiency and optimization.",
        "general": "You are ValyxoGPT, powered by Zencoder. Provide helpful development guidance and coding assistance."
    }

    def __init__(self) -> None:
        """Initialize GPT module with API key and message history."""
        self.messages: List[Dict[str, str]] = []
        self.api_key: Optional[str] = self._load_api_key()
        self.conversation_count: int = 0
        self.last_category: str = "general"

    def _load_api_key(self) -> Optional[str]:
        """Load API key from configuration file.
        
        Returns:
            API key string if found, None otherwise
        """
        if not os.path.exists(API_KEY_PATH):
            return None
        
        try:
            with open(API_KEY_PATH, "r", encoding="utf-8") as f:
                key = f.read().strip()
                return key if key else None
        except (OSError, IOError) as e:
            print(f"Warning: Could not load API key: {e}")
            return None

    def set_api_key(self, key: str) -> bool:
        """Save API key to configuration file.
        
        Args:
            key: API key to save
        
        Returns:
            True if successful, False otherwise
        """
        self.api_key = key
        try:
            os.makedirs(CONFIG_DIR, exist_ok=True)
            with open(API_KEY_PATH, "w", encoding="utf-8") as f:
                f.write(key)
            return True
        except (OSError, IOError) as e:
            print(f"Error: Could not save API key: {e}")
            return False

    def add_message(self, role: str, content: str) -> None:
        """Add message to conversation history.
        
        Args:
            role: Message role ('user' or 'assistant')
            content: Message content
        """
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.MAX_HISTORY:
            self.messages = self.messages[-self.MAX_HISTORY:]

    def get_response(self, user_input: str) -> str:
        """Get AI response to user input with context awareness.
        
        Args:
            user_input: User's question or request
        
        Returns:
            AI response string
        """
        self.add_message("user", user_input)
        self.conversation_count += 1
        reply = self._zencoder_response(user_input)
        self.add_message("assistant", reply)
        return reply
    
    def _categorize_query(self, user_text: str) -> str:
        """Categorize user query to select appropriate response strategy.
        
        Args:
            user_text: User's input text
        
        Returns:
            Category name
        """
        lower = user_text.lower()
        
        if any(word in lower for word in ["valyxoscript", "vscript", "set ", "print ", "for ", "while "]):
            return "valyxoscript"
        elif any(word in lower for word in ["debug", "error", "bug", "fix", "wrong", "broken"]):
            return "debugging"
        elif any(word in lower for word in ["optimize", "performance", "slow", "efficient"]):
            return "performance"
        elif any(word in lower for word in ["code", "function", "variable", "class", "loop"]):
            return "coding"
        else:
            return "general"
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.messages = []
        self.conversation_count = 0
        self.last_category = "general"

    def _zencoder_response(self, user_text: str) -> str:
        """Generate contextual response based on user input.
        
        Uses category-specific responses with fallback to general assistance.
        
        Args:
            user_text: User's input text
        
        Returns:
            Relevant AI response
        """
        if not user_text:
            return "I'm ValyxoGPT powered by Zencoder. Ask me about coding, ValyxoScript, or any development task!"
        
        lower = user_text.lower()
        category = self._categorize_query(user_text)
        self.last_category = category
        
        if category == "valyxoscript":
            return self._respond_valyxoscript(lower)
        elif category == "debugging":
            return self._respond_debugging(lower)
        elif category == "performance":
            return self._respond_performance(lower)
        elif category == "coding":
            return self._respond_coding(lower)
        else:
            return self._respond_general(lower)
    
    def _respond_valyxoscript(self, lower: str) -> str:
        """Generate ValyxoScript-specific response."""
        if "function" in lower or "func" in lower:
            return "ValyxoScript functions: Use 'func name(params) { body }' to define. Call with 'name(args)'. Supports parameters and local scope."
        if "loop" in lower or "for" in lower or "while" in lower:
            return "ValyxoScript loops: 'while [condition] { body }' or 'for i in start to end { body }'. Both support infinite loop protection (max 10k iterations)."
        if "variable" in lower or "set " in lower:
            return "ValyxoScript variables: Use 'set name = value' to create. Supports numbers, strings, booleans. Type inference is automatic."
        if "print" in lower:
            return "ValyxoScript printing: Use 'print variable' or 'print \"text\"' or 'print expression'. Multiple values: 'print a, b, c'."
        if "if" in lower or "condition" in lower:
            return "ValyxoScript conditionals: 'if [condition] then [cmd] else [cmd]' for inline, or 'if [condition] { body }' for blocks."
        return "ValyxoScript v0.5.1: Lightweight language with variables, loops, functions, and control flow. Type: 'enter ValyxoScript' to start coding!"
    
    def _respond_debugging(self, lower: str) -> str:
        """Generate debugging-specific response."""
        if "error" in lower or "exception" in lower:
            return "To debug errors: 1) Read the error message carefully, 2) Check line numbers, 3) Verify variable definitions, 4) Test small parts separately."
        if "infinite" in lower:
            return "Infinite loop detected? ValyxoScript has loop protection (max 10k iterations). Check your while condition or for range carefully."
        if "undefined" in lower or "not defined" in lower:
            return "Undefined variable error: Make sure to 'set variable = value' before using it. Check spelling and scope."
        return "Debugging tips: Add print statements to trace execution, check variable values with 'vars' command, isolate the problem area."
    
    def _respond_performance(self, lower: str) -> str:
        """Generate performance-specific response."""
        if "loop" in lower:
            return "Loop optimization: Avoid unnecessary iterations, use appropriate loop type (for vs while), minimize operations inside loops."
        if "memory" in lower:
            return "Memory optimization: Reuse variables when possible, avoid large nested data structures, clear unused variables."
        return "Performance tips: Use efficient algorithms, minimize function calls in loops, profile code to find bottlenecks, choose right data structures."
    
    def _respond_coding(self, lower: str) -> str:
        """Generate general coding-specific response."""
        if "best practice" in lower or "clean code" in lower:
            return "Clean code principles: Use meaningful names, keep functions small, write comments, follow consistent style, test thoroughly."
        if "refactor" in lower or "improve" in lower:
            return "Code refactoring: Extract functions, reduce duplication, improve readability, add type hints, test after changes."
        if "test" in lower:
            return "Testing: Write unit tests for functions, test edge cases, use assertions, automate testing, maintain test quality."
        return "Coding help: I can assist with code generation, refactoring, debugging, testing, and best practices. Share your code!"
    
    def _respond_general(self, lower: str) -> str:
        """Generate general response."""
        if "hello" in lower or "hi" in lower or "hey" in lower:
            return "Hello! I'm ValyxoGPT v0.5.1, powered by Zencoder. I help with code generation, debugging, refactoring, testing, and ValyxoScript guidance."
        if any(word in lower for word in ["what", "how", "why", "explain", "understand"]):
            return "I can help explain: ValyxoScript syntax, coding concepts, debugging strategies, best practices, and development workflows."
        if "help" in lower or "?" in lower:
            return "I can assist with: ValyxoScript programming, code generation, debugging, refactoring, testing, and development questions."
        preview = lower[:40].strip() + ("..." if len(lower) > 40 else "")
        return f"About '{preview}': How can I help with your coding or development needs?"
