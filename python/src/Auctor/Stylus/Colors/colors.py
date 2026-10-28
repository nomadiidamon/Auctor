class Colors:
    """ANSI escape sequences"""

    HEADER = "\033[95m"
    FAIL = "\033[91m"
    WARNING = "\033[93m"
    OKGREEN = "\033[92m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKYELLOW = "\033[93m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    ITALICS = "\033[3m"
    UNDERLINE = "\033[4m"


def Style(text: str, *codes: str) -> str:
    """Wrap text in the given ANSI codes and reset; no codes returns the text unchanged."""
    if not codes:
        return text
    return "".join(codes) + text + Colors.ENDC
