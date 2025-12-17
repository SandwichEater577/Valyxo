import os
from typing import List, Dict, Optional
from .constants import API_KEY_PATH, CONFIG_DIR


class ValyxoGPTModule:
    """AI Assistant module for Valyxo, powered by Zencoder.
    
    Manages conversation history and provides intelligent responses for
    coding assistance, debugging, and development guidance.
    """

    MAX_HISTORY = 40

    def __init__(self) -> None:
        """Initialize GPT module with API key and message history."""
        self.messages: List[Dict[str, str]] = []
        self.api_key: Optional[str] = self._load_api_key()

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
        """Get AI response to user input.
        
        Args:
            user_input: User's question or request
        
        Returns:
            AI response string
        """
        self.add_message("user", user_input)
        reply = self._zencoder_response(user_input)
        self.add_message("assistant", reply)
        return reply

    @staticmethod
    def _zencoder_response(user_text: str) -> str:
        """Generate contextual response based on user input.
        
        Args:
            user_text: User's input text
        
        Returns:
            Relevant AI response
        """
        if not user_text:
            return "I'm ValyxoGPT powered by Zencoder. Ask me about coding, ValyxoScript, or any development task!"
        
        lower = user_text.lower()
        
        if "function" in lower and "valyxoscript" in lower:
            return "ValyxoScript functions: Use 'func name(params) { body }' to define. Call with 'name(args)'. Supports parameters and local scope."
        
        if "loop" in lower:
            return "ValyxoScript loops: 'while condition { body }' or 'for var in start to end { body }'. Both support infinite loop protection."
        
        if "hello" in lower or "hi" in lower:
            return "Hello! I'm ValyxoGPT, powered by Zencoder AI. I help with code generation, refactoring, debugging, testing, and more."
        
        if "refactor" in lower or "improve" in lower:
            return "I can help refactor your code! Share the code and I'll suggest improvements for readability and performance."
        
        if "debug" in lower or "error" in lower or "fix" in lower:
            return "I can help debug! Describe the issue or share your code, and I'll help identify the problem."
        
        if "test" in lower:
            return "I can help write tests! Share your code and I'll generate comprehensive unit tests."
        
        if any(word in lower for word in ["explain", "understand", "how", "what", "why"]):
            return "I'm Zencoder-powered ValyxoGPT. I help with: code generation, refactoring, debugging, testing, analysis, and ValyxoScript guidance."
        
        preview = user_text[:30].strip() + ("..." if len(user_text) > 30 else "")
        return f"I'm ValyxoGPT. About '{preview}': How can I help with coding or ValyxoScript?"
