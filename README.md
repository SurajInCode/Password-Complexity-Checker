<h1 align="center">Password Complexity Checker</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge">
  <img src="https://img.shields.io/badge/Tkinter-%2320232a.svg?style=for-the-badge&logo=gui&logoColor=white" alt="Tkinter Badge">
</p>

<p align="center">
  A desktop GUI app to evaluate password strength, generate random passwords, and copy them to the clipboard.
</p>

## Features

- **Password strength evaluation** — Character breakdown (lowercase, uppercase, digits, spaces, symbols), length, and estimated entropy with feedback labels.
- **Live feedback** — Strength updates as you type.
- **Generate passwords** — Creates a 16-character password using Python's `secrets` module (letters, digits, and punctuation).
- **Copy to clipboard** — Copies the current password via `pyperclip` (requires a clipboard backend on Linux).
- **Show / hide password** — Toggle visibility in the entry field.
- **Progress bar** — Visual indicator colored by a character-type score.

## Requirements

- **Python 3.8+** (stdlib includes Tkinter on most installs; on some Linux distros install `python3-tk` separately).
- **[pyperclip](https://pypi.org/project/pyperclip/)** — Used for the Copy Password action.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/SurajInCode/Password-Complexity-Checker.git
   cd Password-Complexity-Checker
   ```

2. (Recommended) Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install pyperclip
   ```

   On Linux, if copy fails, install a clipboard helper (for example `xclip` or `xsel` on X11).

## Usage

Run the application from the project root:

```bash
python main.py
```

1. Type a password in the field (or click **Generate Password**).
2. Review the analysis in the text area and the progress bar.
3. Use **Copy Password** to copy the value to the clipboard, or **Clear** to reset.

## Project structure

```
Password-Complexity-Checker/
├── main.py              # Application logic and Tkinter GUI
├── files/
│   ├── pic.ico          # App icon asset
│   └── screenshot.png   # README screenshot
└── README.md
```

## How strength is estimated

The app reports:

- A **character-type score** (used for the progress bar): points for lowercase, uppercase, digits, spaces, symbols, and extra credit for length ≥ 12.
- **Estimated entropy** (bits): `length × log₂(charset_size)`, where `charset_size` is the sum of sizes of character classes present in the password.

Remarks (Very Weak → Excellent) are based on entropy thresholds. This is a simplified heuristic, not a full password-cracking model. For production systems, consider dedicated libraries (for example [zxcvbn](https://github.com/dropbox/zxcvbn)) or breach checks.

## Screenshots

![App Screenshot](files/screenshot.png)

## Contributing

Contributions are welcome. Please open an issue or submit a pull request with a clear description of the change.

## License

This project is intended to be licensed under the [MIT License](LICENSE).

## Author

**SurajInCode**

<p align="center">
  <a href="https://github.com/SurajInCode">
    <img src="https://img.shields.io/badge/Visit%20My%20Profile-%23121011.svg?style=for-the-badge&logo=github&logoColor=white" alt="Visit My Profile">
  </a>
</p>

<p align="center">
  <a href="https://linkedin.com/in/suraj5045">
    <img src="https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white" alt="LinkedIn Badge">
  </a>
  <a href="https://github.com/SurajInCode">
    <img src="https://img.shields.io/badge/GitHub-%23121011.svg?logo=github&logoColor=white" alt="GitHub Badge">
  </a>
  <a href="https://www.instagram.com/suraj.h.e/">
    <img src="https://img.shields.io/badge/Instagram-%23E4405F.svg?logo=instagram&logoColor=white" alt="Instagram Badge">
  </a>
</p>

<p align="center">
  <a href="https://github.com/SurajInCode">
    <img src="files/pic.ico" alt="Icon" width="50" height="50">
  </a>
</p>
