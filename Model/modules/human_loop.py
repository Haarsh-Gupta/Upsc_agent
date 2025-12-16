def human_verify(text):
    print("\n--- OCR EXTRACTED TEXT ---\n")
    print(text)
    print("\nPress Enter to confirm or type corrections. End with 'END'.")
    inp = input().strip()

    if inp == "":
        return text

    corrected = []
    print("Start typing corrected text:")
    while True:
        line = input()
        if line.strip() == "END":
            break
        corrected.append(line)

    return "\n".join(corrected)
