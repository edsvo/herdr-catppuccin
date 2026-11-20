#!/usr/bin/env python3
"""Print the Herdr screen used for the theme previews."""

import sys

flavor = sys.argv[1] if len(sys.argv) > 1 else "mocha"
reset = "\033[0m"
bold = "\033[1m"
dim = "\033[2m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"

print("\033]0;t4\007", end="")
print("\033[2J\033[H", end="")

print(f"{dim}Theme{reset}    {bold}catppuccin-{flavor}{reset}")
print(f"{dim}Font{reset}     IBM Plex Mono")
print()
print(f"{magenta}${reset} herdr-app do app.theme --name {bold}catppuccin-{flavor}{reset}")
print()
print(
    f"{blue}working{reset}   "
    f"\033[31mblocked{reset}   "
    f"{green}done{reset}   "
    f"{dim}idle{reset}   "
    f"{dim}unknown{reset}"
)
print()
print(f"{dim}ANSI palette{reset}")
print("".join(f"\033[{code}m  {reset}" for code in (40, 41, 42, 43, 44, 45, 46, 47)))
print("".join(f"\033[{code}m  {reset}" for code in (100, 101, 102, 103, 104, 105, 106, 107)))
print()
print(f"{blue}def{reset} {yellow}greet{reset}(name: {blue}str{reset}) -> {blue}str{reset}:")
print(f"    {dim}# A soothing pastel theme for the high-spirited{reset}")
print(f"    {green}return{reset} {green}f\"Hello, {{name}}!\"{reset}")
print()
print(f"{dim}FILE                     STATUS      SIZE{reset}")
print(f"catppuccin-latte.json    {green}done{reset}        1.0 KB")
print(f"catppuccin-mocha.json    {green}done{reset}        1.0 KB")
print(f"generate.py              {blue}working{reset}     16 KB")
print(f"{dim}--------------------------------------------{reset}")
print()
print("herdr-catppuccin/")
print("  themes/")
print("    catppuccin-latte.json")
print("    catppuccin-frappe.json")
print("    catppuccin-macchiato.json")
print("    catppuccin-mocha.json")
print("  scripts/generate.py")
print("  README.md")
print("  PREVIEWS.md")
print()
print(f"{green}4 flavors{reset}  {dim}|  24 color tokens  |  16 ANSI colors{reset}")
print()
print(f"{magenta}Soothing pastel theme for Herdr{reset}")
print()
print(f"{green}${reset} ", end="", flush=True)
