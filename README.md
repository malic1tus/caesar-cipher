
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
    
-   Output: `Khoor#Zruog`
    

#### Decryption:

-   Input: `Khoor#Zruog`
    
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
    E1 --> F1[Convert to Unicode Value]
    F1 --> G1[Add Shift Value]
    G1 --> H1[Apply Modulo 256]
    H1 --> I1[Convert Back to Character]
    I1 --> J1[Append to Result]
    J1 --> K1{More Characters?}
    K1 -->|Yes| E1
    K1 -->|No| L1[Combine Result]
    
    %% Decryption Path
    D2 --> E2[Iterate Through Each Character]
    E2 --> F2[Convert to Unicode Value]
    F2 --> G2[Subtract Shift Value]
    G2 --> H2[Apply Modulo 256]
    H2 --> I2[Convert Back to Character]
    I2 --> J2[Append to Result]
    J2 --> K2{More Characters?}
    K2 -->|Yes| E2
    K2 -->|No| L2[Combine Result]
    
    L1 --> M1[Encrypted Text]
    L2 --> M2[Decrypted Text]
    M1 & M2 --> N[End]

    %% Add notes for clarity
    subgraph "Character Support"
        Note1[Supports all printable characters]
        Note2[Including accented letters]
        Note3[Symbols and numbers]
        Note4[Uses Unicode values]
    end
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