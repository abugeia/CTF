def decrypt(ciphertext):
    decrypted_text = ""
    for char in ciphertext:
        decrypted_char = chr(ord(char) - 1)
        decrypted_text += decrypted_char
        print(f"char: {char}, decrypted_char: {decrypted_char}") # Debug print
    return decrypted_text

def main():
    with open("writes_up/sunshinectf_2025/Roman Romance/enc.txt", "r") as f:
        ciphertext = f.read().strip()
    
    decrypted_text = decrypt(ciphertext)
    print(decrypted_text)

if __name__ == "__main__":
    main()