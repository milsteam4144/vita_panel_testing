#!/usr/bin/env python3
"""
VITA Console Demo - Terminal version of the Panel app
Uses the same core logic as the web version
"""
import asyncio
import os
import sys
from pathlib import Path
from vita_core import VitaCore

class VitaConsole:
    """Console interface for VITA"""
    
    def __init__(self):
        self.vita = VitaCore(message_callback=self.display_message)
        self.user_input_future = None
        
        # Override the human input method for console
        self.vita.user_proxy.a_get_human_input = self.get_console_input
        
    def display_message(self, sender_name: str, content: str, avatar: str):
        """Display agent messages in console format"""
        print(f"\n{avatar} {sender_name}:")
        print("=" * (len(sender_name) + 4))
        print(content)
        print("-" * 60)
    
    async def get_console_input(self, prompt: str) -> str:
        """Get input from user in console"""
        print(f"\n🤔 {prompt}")
        print("Your response (or 'exit' to end): ", end="")
        
        # Create a future for input
        loop = asyncio.get_event_loop()
        self.user_input_future = loop.create_future()
        
        # In a real implementation, you'd want proper async input
        # For now, we'll use a simple approach
        try:
            user_input = input()
            return user_input
        except KeyboardInterrupt:
            return "exit"
    
    def display_welcome(self):
        """Display welcome message"""
        print("=" * 60)
        print("🎓 VITA: Virtual Interactive Teaching Assistant")
        print("=" * 60)
        print("Console Demo Version")
        print("This demo uses the same core logic as the web version.")
        print("-" * 60)
    
    def display_file_with_numbers(self, content: str):
        """Display file content with line numbers"""
        print("\n📁 Uploaded File Content:")
        print("=" * 30)
        numbered_content = self.vita.process_file(content)
        print(numbered_content)
        print("=" * 30)
    
    async def run_interactive(self):
        """Run interactive console session"""
        self.display_welcome()
        
        while True:
            print("\n" + "=" * 60)
            print("VITA Console Menu:")
            print("1. Load Python file for debugging")
            print("2. Enter code directly")
            print("3. Run test with sample buggy code")
            print("4. Exit")
            print("-" * 60)
            
            try:
                choice = input("Enter your choice (1-4): ").strip()
                
                if choice == "1":
                    await self.load_file_session()
                elif choice == "2":
                    await self.direct_code_session()
                elif choice == "3":
                    await self.test_session()
                elif choice == "4":
                    print("\n👋 Thanks for using VITA! Goodbye!")
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    async def load_file_session(self):
        """Load and debug a Python file"""
        print("\n📁 File Loading Session")
        print("-" * 30)
        
        file_path = input("Enter the path to your Python file: ").strip()
        
        try:
            path = Path(file_path)
            if not path.exists():
                print(f"❌ File not found: {file_path}")
                return
                
            if not path.suffix == '.py':
                print("⚠️  Warning: File doesn't have .py extension")
                
            content = path.read_text()
            self.display_file_with_numbers(content)
            
            print(f"\n🚀 Starting debugging session for {path.name}...")
            await self.vita.start_debug_session(content)
            
        except Exception as e:
            print(f"❌ Error reading file: {e}")
    
    async def direct_code_session(self):
        """Enter code directly in console"""
        print("\n✏️  Direct Code Entry Session")
        print("-" * 30)
        print("Enter your Python code (press Ctrl+D when done, Ctrl+C to cancel):")
        print("-" * 30)
        
        lines = []
        try:
            while True:
                try:
                    line = input()
                    lines.append(line)
                except EOFError:
                    break
                    
            content = '\n'.join(lines)
            if content.strip():
                self.display_file_with_numbers(content)
                print(f"\n🚀 Starting debugging session...")
                await self.vita.start_debug_session(content)
            else:
                print("❌ No code entered.")
                
        except KeyboardInterrupt:
            print("\n❌ Code entry cancelled.")
    
    async def test_session(self):
        """Run with sample buggy code"""
        print("\n🧪 Test Session with Sample Code")
        print("-" * 30)
        
        sample_codes = {
            "1": {
                "name": "Mismatched Quotes",
                "code": 'print("hello world\')\nprint("test")'
            },
            "2": {
                "name": "Missing Parentheses", 
                "code": 'print "hello world"\nx = 5'
            },
            "3": {
                "name": "Indentation Error",
                "code": 'if True:\nprint("indented")\n  print("wrong indent")'
            },
            "4": {
                "name": "Undefined Variable",
                "code": 'print(hello)\nx = world + 5'
            }
        }
        
        print("Sample buggy code options:")
        for key, value in sample_codes.items():
            print(f"{key}. {value['name']}")
            
        choice = input("\nSelect sample code (1-4): ").strip()
        
        if choice in sample_codes:
            sample = sample_codes[choice]
            print(f"\n📝 Testing with: {sample['name']}")
            self.display_file_with_numbers(sample['code'])
            print(f"\n🚀 Starting debugging session...")
            await self.vita.start_debug_session(sample['code'])
        else:
            print("❌ Invalid choice.")

def main():
    """Main entry point"""
    # Set environment for local model by default
    if "USE_LOCAL_MODEL" not in os.environ:
        os.environ["USE_LOCAL_MODEL"] = "true"
    
    console = VitaConsole()
    
    try:
        asyncio.run(console.run_interactive())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()