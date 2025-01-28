
# Caesar Cipher Encryption

This project provides a Python program to encrypt and decrypt text using the **Caesar cipher**. This cipher is a substitution method where each letter is replaced by another located a fixed distance away in the alphabet.

----------

## Features

-   Encrypt text with a specified shift.
    
-   Decrypt text that has been previously encrypted.
    
-   Simple command-line interface.
    

----------

## Prerequisites

-   Python 3 or higher.
    

----------

## Installation

1.  Clone the repository:
    

```
git clone https://github.com/malic1tus/caesar-cipher
```

2.  Navigate to the directory:
    

```
cd caesar-cipher
```

----------

## Usage

1.  Run the program:
    

```
python caesar_cipher.py
```

2.  Follow the terminal instructions to:
    
    -   Encrypt text.
        
    -   Decrypt text.
        
    -   Exit the program.
        

### Example:

#### Encryption:

-   Input: `Hello World`
    
-   Shift: `3`
    
-   Output: `Khoor Zruog`
    

#### Decryption:

-   Input: `Khoor Zruog`
    
-   Shift: `3`
    
-   Output: `Hello World`
    

----------

## Project Structure

-   `caesar_cipher.py`: Contains the main code for encryption and decryption.
    

----------

## Flowchart

Below is a flowchart representing how the Caesar cipher encryption works:

```mermaid
---
config:
  layout: fixed
  theme: neo-dark
  look: handDrawn
---
graph TD
    A[Start] --> B[Input Text]
    B --> C[Input Shift Value]
    C --> D1[Encrypt Process] & D2[Decrypt Process]
    
    %% Encryption Path
    D1 --> E1[Iterate Through Each Character]
    E1 --> F1{Is Character Alphabetic?}
    F1 -->|Yes| G1[Shift Character Forward by Value]
    F1 -->|No| H1[Keep Character As Is]
    G1 & H1 --> I1[Append to Result]
    I1 --> J1{More Characters?}
    J1 -->|Yes| E1
    J1 -->|No| K1[Combine Result]
    
    %% Decryption Path
    D2 --> E2[Iterate Through Each Character]
    E2 --> F2{Is Character Alphabetic?}
    F2 -->|Yes| G2[Shift Character Backward by Value]
    F2 -->|No| H2[Keep Character As Is]
    G2 & H2 --> I2[Append to Result]
    I2 --> J2{More Characters?}
    J2 -->|Yes| E2
    J2 -->|No| K2[Combine Result]
    
    K1 --> L1[Encrypted Text]
    K2 --> L2[Decrypted Text]
    L1 & L2 --> M[End]
```

----------

## Contribution

Contributions are welcome!

1.  Fork the repository.
    
2.  Create a branch: `git checkout -b feature-new-functionality`
    
3.  Make your changes.
    
4.  Push your changes: `git push origin feature-new-functionality`
    
5.  Create a Pull Request.
    

----------

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.