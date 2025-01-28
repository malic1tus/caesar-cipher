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

def main():
    print("Welcome to the Extended Caesar Cipher program!")
    while True:
        print("\nChoose an option:")
        print("1 - Encrypt a text")
        print("2 - Decrypt a text")
        print("3 - Exit")
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
            print("Thank you for using the program. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()