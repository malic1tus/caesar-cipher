import os
import json
from datetime import datetime
from typing import Optional, Dict, List
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from rich.logging import RichHandler
import logging
import string
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

log = logging.getLogger("caesar_cipher")
console = Console()

class CaesarCipher:
    """Class handling the Caesar cipher encryption/decryption logic."""
    
    def __init__(self):
        self.history: List[Dict] = []
        self.history_file = Path("cipher_history.json")
        self._load_history()

    def _load_history(self) -> None:
        """Load operation history from file."""
        try:
            if self.history_file.exists():
                with open(self.history_file, "r") as f:
                    self.history = json.load(f)
        except Exception as e:
            log.error(f"Error loading history: {e}")
            self.history = []

    def _save_history(self) -> None:
        """Save operation history to file."""
        try:
            with open(self.history_file, "w") as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            log.error(f"Error saving history: {e}")

    def _add_to_history(self, operation: str, input_text: str, output_text: str, shift: int) -> None:
        """Add an operation to history."""
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "input_text": input_text,
            "output_text": output_text,
            "shift": shift
        })
        self._save_history()

    @staticmethod
    def validate_shift(shift: int) -> int:
        """Validate and normalize the shift value."""
        return shift % 256

    def encrypt(self, text: str, shift: int) -> str:
        """Encrypt text using Caesar cipher."""
        if not text:
            raise ValueError("Text cannot be empty")
            
        shift = self.validate_shift(shift)
        encrypted = ""
        
        try:
            for char in text:
                if char.isprintable():
                    encrypted += chr((ord(char) + shift) % 256)
                else:
                    encrypted += char
                    
            self._add_to_history("encrypt", text, encrypted, shift)
            return encrypted
            
        except Exception as e:
            log.error(f"Encryption error: {e}")
            raise

    def decrypt(self, text: str, shift: int) -> str:
        """Decrypt text using Caesar cipher."""
        return self.encrypt(text, -shift)

    def analyze_frequency(self, text: str) -> Dict[str, float]:
        """Analyze character frequency in text."""
        if not text:
            return {}
            
        freq = {}
        total = len(text)
        
        for char in text:
            if char in freq:
                freq[char] += 1
            else:
                freq[char] = 1
                
        return {k: v/total for k, v in freq.items()}

    def bruteforce_decrypt(self, text: str) -> List[Dict]:
        """Attempt to decrypt text using all possible shifts."""
        results = []
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Trying all shifts...", total=256)
            
            for shift in range(256):
                decrypted = self.decrypt(text, shift)
                freq = self.analyze_frequency(decrypted)
                
                # Simple scoring based on common English letters
                score = sum(freq.get(c, 0) for c in string.ascii_letters + string.whitespace)
                
                results.append({
                    "shift": shift,
                    "text": decrypted,
                    "score": score
                })
                
                progress.update(task, advance=1)
                
        # Sort results by score, highest first
        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    def process_file(self, input_path: str, output_path: str, shift: int, encrypt: bool = True) -> None:
        """Process an entire file."""
        try:
            with open(input_path, 'r') as f:
                text = f.read()
                
            processed = self.encrypt(text, shift) if encrypt else self.decrypt(text, shift)
            
            with open(output_path, 'w') as f:
                f.write(processed)
                
            log.info(f"File processed successfully: {output_path}")
            
        except Exception as e:
            log.error(f"File processing error: {e}")
            raise

def display_menu() -> None:
    """Display the main menu."""
    console.print("\n[bold yellow]Choose an option:[/bold yellow]")
    console.print("[bold green]1[/bold green] - 🔒 Encrypt a text")
    console.print("[bold green]2[/bold green] - 🔓 Decrypt a text")
    console.print("[bold green]3[/bold green] - 🔄 Bruteforce decrypt")
    console.print("[bold green]4[/bold green] - 📁 Process file")
    console.print("[bold green]5[/bold green] - 📊 View history")
    console.print("[bold green]6[/bold green] - ❌ Exit")

def display_results_table(results: List[Dict], limit: int = 10) -> None:
    """Display decryption results in a table."""
    table = Table(title="Decryption Results", show_header=True, header_style="bold magenta")
    table.add_column("Shift", justify="right")
    table.add_column("Score", justify="right")
    table.add_column("Decrypted Text", overflow="fold")
    
    for result in results[:limit]:
        table.add_row(
            str(result["shift"]),
            f"{result['score']:.3f}",
            result["text"][:50] + ("..." if len(result["text"]) > 50 else "")
        )
        
    console.print(table)

def display_history(cipher: CaesarCipher) -> None:
    """Display operation history."""
    if not cipher.history:
        console.print("[yellow]No history available[/yellow]")
        return
        
    table = Table(title="Operation History", show_header=True, header_style="bold magenta")
    table.add_column("Timestamp", justify="left")
    table.add_column("Operation", justify="center")
    table.add_column("Input", overflow="fold")
    table.add_column("Output", overflow="fold")
    table.add_column("Shift", justify="right")
    
    for entry in reversed(cipher.history[-10:]):  # Show last 10 entries
        table.add_row(
            entry["timestamp"].split("T")[0],
            entry["operation"],
            entry["input_text"][:20] + "...",
            entry["output_text"][:20] + "...",
            str(entry["shift"])
        )
        
    console.print(table)

def main():
    """Main program loop."""
    cipher = CaesarCipher()
    console.print(Panel("[bold cyan]Welcome to the Enhanced Caesar Cipher Program![/bold cyan]", expand=False))

    while True:
        try:
            display_menu()
            choice = Prompt.ask("Your choice", choices=["1", "2", "3", "4", "5", "6"], default="6")

            if choice == '1':  # Encrypt
                text = Prompt.ask("Enter the text to encrypt")
                shift = IntPrompt.ask("Enter the shift value", default=3)
                encrypted_text = cipher.encrypt(text, shift)
                console.print(Panel(f"[bold green]Encrypted text:[/bold green] {encrypted_text}", expand=False))

            elif choice == '2':  # Decrypt
                text = Prompt.ask("Enter the text to decrypt")
                shift = IntPrompt.ask("Enter the shift value used for encryption", default=3)
                decrypted_text = cipher.decrypt(text, shift)
                console.print(Panel(f"[bold green]Decrypted text:[/bold green] {decrypted_text}", expand=False))

            elif choice == '3':  # Bruteforce
                text = Prompt.ask("Enter the encrypted text to bruteforce")
                results = cipher.bruteforce_decrypt(text)
                display_results_table(results)

            elif choice == '4':  # Process file
                input_path = Prompt.ask("Enter input file path")
                output_path = Prompt.ask("Enter output file path")
                shift = IntPrompt.ask("Enter shift value", default=3)
                operation = Prompt.ask("Choose operation", choices=["encrypt", "decrypt"], default="encrypt")
                
                cipher.process_file(input_path, output_path, shift, operation == "encrypt")
                console.print(f"[green]File processed successfully: {output_path}[/green]")

            elif choice == '5':  # View history
                display_history(cipher)

            elif choice == '6':  # Exit
                console.print("[bold cyan]Thank you for using the program. Goodbye![/bold cyan]")
                break

        except Exception as e:
            log.error(f"An error occurred: {e}")
            console.print(f"[bold red]Error:[/bold red] {str(e)}")

if __name__ == "__main__":
    main()