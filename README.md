# autotype

Extract text from a PDF and type it into a focused window using a hotkey trigger.

## Installation

```bash
conda env create -f environment.yml
conda activate your-env-name
pip install -e .
autotype
```

## Usage

```bash
autotype document.pdf
autotype document.pdf --hotkey f9
autotype document.pdf --hotkey f9 --interval 0.02
autotype document.pdf --hotkey f9 --interval 0.02 --keep-newlines
```

### Arguments

| Argument | Description | Default |
|---|---|---|
| `pdf` | Path to the PDF file to read (required) | — |
| `--hotkey` | Key that triggers typing to start | `f8` |
| `--interval` | Delay in seconds between keystrokes | `0.05` |
| `--keep-newlines` | Keep newline characters instead of stripping them | off (newlines stripped) |

## Notes

`pyautogui.typewrite()` handles `\n` by pressing Enter, so with `--keep-newlines` it will insert actual line breaks as it types. This is useful for forms and editors, but it could submit a form early if Enter triggers a submit action there. Worth keeping in mind depending on what field you're typing into.
