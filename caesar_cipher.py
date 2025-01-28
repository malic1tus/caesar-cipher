from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel

console = Console()

def caesar_encrypt(text, shift):
    """Encrypts text using Caesar cipher with a given shift, including accented characters, symbols, and numbers."""
    encrypted = ""
    for char in text:
        if char.isprintable():
            # Shift all printable characters
            encrypted += chr((ord(char) + shift) % 256)
        else:
            encrypted += char
    return encrypted

def caesar_decrypt(text, shift):
    """Decrypts text encrypted using Caesar cipher with a given shift, including accented characters, symbols, and numbers."""
    return caesar_encrypt(text, -shift)

def bruteforce_decrypt(text):
    """Attempts to decrypt text by trying all possible shift values."""
    table = Table(title="Bruteforce Results", show_header=True, header_style="bold magenta")
    table.add_column("Shift", justify="right")
    table.add_column("Decrypted Text", overflow="fold")

    for shift in range(256):  # Try all possible shifts (0-255)
        decrypted = caesar_decrypt(text, shift)
        table.add_row(str(shift), decrypted[:50] + ("..." if len(decrypted) > 50 else ""))

    console.print(table)

def main():
    console.print(Panel("[bold cyan]Welcome to the Extended Caesar Cipher Program![/bold cyan]", expand=False))

    while True:
        console.print("\n[bold yellow]Choose an option:[/bold yellow]")
        console.print("[bold green]1[/bold green] - 🔒 Encrypt a text")
        console.print("[bold green]2[/bold green] - 🔓 Decrypt a text")
        console.print("[bold green]3[/bold green] - 🔄 Bruteforce decrypt")
        console.print("[bold green]4[/bold green] - ❌ Exit")

        choice = Prompt.ask("Your choice", choices=["1", "2", "3", "4"], default="4")

        if choice == '1':
            text = Prompt.ask("Enter the text to encrypt")
            shift = int(Prompt.ask("Enter the shift value (integer)", default="0"))
            encrypted_text = caesar_encrypt(text, shift)
            console.print(Panel(f"[bold green]Encrypted text:[/bold green] {encrypted_text}", expand=False))

        elif choice == '2':
            text = Prompt.ask("Enter the text to decrypt")
            shift = int(Prompt.ask("Enter the shift value used for encryption", default="0"))
            decrypted_text = caesar_decrypt(text, shift)
            console.print(Panel(f"[bold green]Decrypted text:[/bold green] {decrypted_text}", expand=False))

        elif choice == '3':
            text = Prompt.ask("Enter the encrypted text to bruteforce")
            bruteforce_decrypt(text)

        elif choice == '4':
            console.print("[bold cyan]Thank you for using the program. Goodbye![/bold cyan]")
            break

if __name__ == "__main__":
    main()
