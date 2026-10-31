"""Magic UI Terminal Demo in Pure Python.

Run directly in your terminal (PowerShell, CMD, bash):
    python scripts/terminal_demo.py

Requires zero node modules and zero external packages (pure standard library).
"""

import sys
import time
import os

# Enable UTF-8 encoding for Windows standard output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ANSI color codes for cross-platform terminals
GREEN = "\033[32m"
BLUE = "\033[34m"
GRAY = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"


def enable_windows_ansi() -> None:
    """Enables virtual terminal processing on Windows if supported."""
    if os.name == "nt":
        os.system("")


def type_text(text: str, delay: float = 0.035, color: str = "") -> None:
    """Simulates character-by-character typing animation."""
    if color:
        sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    if color:
        sys.stdout.write(RESET)
    sys.stdout.write("\n")
    sys.stdout.flush()


def print_span(text: str, color: str = GREEN, delay: float = 0.12) -> None:
    """Prints an animated span line with a delay."""
    sys.stdout.write(f"{color}{text}{RESET}\n")
    sys.stdout.flush()
    time.sleep(delay)


def run_demo() -> None:
    enable_windows_ansi()

    # Terminal box header using ASCII-safe characters
    print(f"\n{GRAY}+-- bash --------------------------------------------------------+{RESET}")
    print(f"{GRAY}|  (*) (*) (*)                                                   |{RESET}")
    print(f"{GRAY}+----------------------------------------------------------------+{RESET}\n")

    # Command typing
    sys.stdout.write("  ")
    type_text("> pnpm dlx shadcn@latest init", delay=0.03, color=BOLD)

    time.sleep(0.15)

    # Animated spans
    steps = [
        "[+] Preflight checks.",
        "[+] Verifying framework. Found Next.js.",
        "[+] Validating Tailwind CSS.",
        "[+] Validating import alias.",
        "[+] Writing components.json.",
        "[+] Checking registry.",
        "[+] Updating tailwind.config.ts",
        "[+] Updating app/globals.css",
        "[+] Installing dependencies.",
    ]

    for step in steps:
        print_span(f"  {step}", color=GREEN, delay=0.1)

    # Blue info block
    print_span("  (i) Updated 1 file:", color=BLUE, delay=0.06)
    print_span("      - lib/utils.ts", color=BLUE, delay=0.12)

    # Success typing animations
    time.sleep(0.12)
    sys.stdout.write("  ")
    type_text("Success! Project initialization completed.", delay=0.02, color=GRAY)
    sys.stdout.write("  ")
    type_text("You may now add components.", delay=0.02, color=GRAY)

    print(f"\n{GRAY}+----------------------------------------------------------------+{RESET}\n")


if __name__ == "__main__":
    run_demo()
