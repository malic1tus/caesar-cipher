import os
import json
from datetime import datetime
from typing import Optional, Dict, List
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.table import Table, box
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
        self.max_history_entries = 100  # Maximum number of entries to store
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
        """Save operation history to file, keeping only the latest 100 entries."""
        try:
            # Keep only the last 100 entries
            if len(self.history) > self.max_history_entries:
                self.history = self.history[-self.max_history_entries:]

            with open(self.history_file, "w") as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            log.error(f"Error saving history: {e}")

    def _add_to_history(self, operation: str, input_text: str, output_text: str, shift: int) -> None:
        """Add an operation to history, keeping the history size in check."""
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
        if not (-255 <= shift <= 255):
            raise ValueError("Shift must be between -255 and 255")
        return shift

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

    def _score_decrypted_text(self, decrypted_text: str) -> float:
        """Calculate a score for the decrypted text based on character frequency."""
        # Utiliser un modèle de fréquence plus général qui prend en compte les caractères spéciaux
        freq = self.analyze_frequency(decrypted_text)
        # Par exemple, on pourrait définir un score basé sur les caractères imprimables et les symboles.
        printable_chars = string.ascii_letters + string.digits + string.punctuation + string.whitespace
        return sum(freq.get(c, 0) for c in printable_chars)

    def bruteforce_decrypt(self, text: str) -> List[Dict]:
        """Attempt to decrypt text using all possible shifts."""
        results = []

        # Nettoyer l'affichage avant de commencer
        console.clear()
        
        # Affichage du message de démarrage
        console.print("\n[bold cyan]Bruteforce decryption in progress...[/bold cyan]\n")
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Trying all shifts...", total=256)

            for shift in range(256):
                decrypted = self.decrypt(text, shift)
                score = self._score_decrypted_text(decrypted)

                results.append({
                    "shift": shift,
                    "text": decrypted,
                    "score": score
                })

                # Mise à jour du progrès
                progress.update(task, advance=1)
            
            # Séparation des résultats de l'entrée utilisateur
            console.print("\n[bold cyan]Bruteforce completed! Here are the top results:[/bold cyan]\n")
        
        # Trier les résultats
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results

    def process_file(self, input_path: str, output_path: str, shift: int, encrypt: bool = True) -> None:
        """Process an entire file."""
        try:
            with open(input_path, 'r') as f:
                lines = f.readlines()
                
            processed_lines = [self.encrypt(line, shift) if encrypt else self.decrypt(line, shift) for line in lines]
            
            with open(output_path, 'w') as f:
                f.writelines(processed_lines)
                
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
    table = Table(
        title="[bold]Decryption Results[/bold]",
        box=None,
        show_header=True,
        header_style="bold magenta",
        padding=(0, 2),
        expand=True
    )
    
    table.add_column("Shift", justify="right", style="cyan", no_wrap=True)
    table.add_column("Score", justify="right", style="green", no_wrap=True)
    table.add_column("Decrypted Text", style="white", overflow="fold", max_width=60)
    
    for result in results[:limit]:
        table.add_row(
            str(result["shift"]),
            f"{result['score']:.3f}",
            result["text"]
        )
        
    console.print("\n")
    console.print(table)
    console.print("\n")

def display_history(cipher: CaesarCipher) -> None:
    """Display operation history."""
    if not cipher.history:
        console.print("[yellow]No history available[/yellow]")
        return
        
    table = Table(
        title="[bold]Operation History[/bold]",
        box=None,
        show_header=True,
        header_style="bold magenta",
        padding=(0, 2),
        expand=True
    )
    
    table.add_column("Timestamp", justify="left", style="cyan", no_wrap=True)
    table.add_column("Operation", justify="center", style="green", no_wrap=True)
    table.add_column("Input", style="white", max_width=30, overflow="fold")
    table.add_column("Output", style="white", max_width=30, overflow="fold")
    table.add_column("Shift", justify="right", style="yellow", no_wrap=True)
    
    for entry in reversed(cipher.history[-10:]):  # Show last 10 entries
        table.add_row(
            entry["timestamp"].split("T")[0],
            entry["operation"],
            entry["input_text"][:30] + ("..." if len(entry["input_text"]) > 30 else ""),
            entry["output_text"][:30] + ("..." if len(entry["output_text"]) > 30 else ""),
            str(entry["shift"])
        )
    
    console.print("\n")
    console.print(table)
    console.print("\n")

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
                cipher.process_file(input_path, output_path, shift, encrypt=(operation == "encrypt"))

            elif choice == '5':  # View history
                display_history(cipher)

            elif choice == '6':  # Exit
                console.print("[bold red]Goodbye![/bold red]")
                break
        except Exception as e:
            log.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
