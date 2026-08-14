import argparse
import re
import sys

import pyautogui
from pynput import keyboard
from pypdf import PdfReader

def extract_text(pdf_path: str, keep_newlines: bool = False) -> str:
    reader = PdfReader(pdf_path)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)

    if keep_newlines:
        text = re.sub(r"[ \t]+", " ", text)          # collapse extra spaces/tabs only
        text = re.sub(r"\n{3,}", "\n\n", text).strip()  # collapse excessive blank lines
    else:
        text = re.sub(r"\s*\n\s*", " ", text)
        text = re.sub(r"\s+", " ", text).strip()

    return text

def type_text(text: str, interval: float = 0.05):
    pyautogui.typewrite(text, interval=interval)

def wait_for_hotkey(hotkey: str):
    key_name = hotkey.lower()

    def on_press(key):
        try:
            if key.char == key_name:
                return False
        except AttributeError:
            if hasattr(keyboard.Key, key_name) and key == getattr(keyboard.Key, key_name):
                return False

    print(f"File {pdf_path} ready. Click into the target field, then press '{hotkey}' to start typing...")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def main():
    parser = argparse.ArgumentParser(
        description="Extract text from a PDF and type it into a focused window."
    )
    parser.add_argument("pdf", help="Path to the PDF file to read")
    parser.add_argument(
        "--hotkey",
        default="f8",
        help="Key that triggers typing to start (default: f8)",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.01,
        help="Delay in seconds between keystrokes (default: 0.01)",
    )
    parser.add_argument(
        "--keep-newlines",
        action="store_true",
        help="Keep newline characters instead of stripping them (default: strip them)",
    )
    args = parser.parse_args()

    try:
        text = extract_text(args.pdf, keep_newlines=args.keep_newlines)
    except FileNotFoundError:
        print(f"Error: file not found: {args.pdf}", file=sys.stderr)
        sys.exit(1)

    if not text:
        print("No text extracted from PDF.", file=sys.stderr)
        sys.exit(1)

    wait_for_hotkey(args.hotkey)
    type_text(text, interval=args.interval)

if __name__ == "__main__":
    main()