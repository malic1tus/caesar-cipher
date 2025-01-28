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
    print("\nBruteforce results:")
    print("-" * 50)
    for shift in range(256):  # Try all possible shifts (0-255)
        decrypted = caesar_decrypt(text, shift)
        print(f"Shift {shift:3d}: {decrypted[:50]}{'...' if len(decrypted) > 50 else ''}")
    print("-" * 50)

def main():
    print("Welcome to the Extended Caesar Cipher program!")
    while True:
        print("\nChoose an option:")
        print("1 - Encrypt a text")
        print("2 - Decrypt a text")
        print("3 - Bruteforce decrypt")
        print("4 - Exit")
        choice = input("Your choice: ")

        if choice == '1':
            text = input("Enter the text to encrypt: ")
            shift = int(input("Enter the shift value (integer): "))
            print("Encrypted text:", caesar_encrypt(text, shift))
        elif choice == '2':
            text = input("Enter the text to decrypt: ")
            shift = int(input("Enter the shift value used for encryption: "))
            print("Decrypted text:", caesar_decrypt(text, shift))
        elif choice == '3':
            text = input("Enter the encrypted text to bruteforce: ")
            bruteforce_decrypt(text)
        elif choice == '4':
            print("Thank you for using the program. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
