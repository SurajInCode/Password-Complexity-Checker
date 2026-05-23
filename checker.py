"""Password strength evaluation and generation."""

from __future__ import annotations

import math
import secrets
import string
from collections import Counter
from dataclasses import dataclass

# Symbols that often break login forms or shell escaping.
SAFE_PUNCTUATION = "!@#$%^&*()-_=+[]{}|;:,.<>?"

COMMON_PASSWORDS = frozenset(
    {
        "password",
        "password1",
        "password123",
        "123456",
        "12345678",
        "123456789",
        "qwerty",
        "abc123",
        "letmein",
        "welcome",
        "monkey",
        "dragon",
        "master",
        "login",
        "admin",
        "passw0rd",
        "iloveyou",
        "sunshine",
        "princess",
        "football",
        "shadow",
        "trustno1",
    }
)

WEAK_SEQUENCES = (
    "0123456789",
    "abcdefghijklmnopqrstuvwxyz",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
)


@dataclass(frozen=True)
class PasswordAnalysis:
    """Result of evaluating a password."""

    report: str
    level: int  # 0 (empty) through 5 (excellent)
    progress: int  # 0–100 for the progress bar
    bar_style: str  # ttk style name


def charset_pool_size(password: str) -> int:
    """Size of the character pool implied by classes present in the password."""
    size = 0
    if any(c in string.ascii_lowercase for c in password):
        size += 26
    if any(c in string.ascii_uppercase for c in password):
        size += 26
    if any(c in string.digits for c in password):
        size += 10
    if any(c in string.punctuation for c in password):
        size += len(string.punctuation)
    return size


def shannon_entropy_per_symbol(password: str) -> float:
    """Shannon entropy in bits per symbol from the observed character distribution."""
    if not password:
        return 0.0
    length = len(password)
    counts = Counter(password)
    return -sum((count / length) * math.log2(count / length) for count in counts.values())


def estimate_entropy_bits(password: str) -> float:
    """
    Estimated guessing entropy in bits.

    Uses the smaller of charset-based and distribution-based estimates so repeated
    or predictable characters lower the score.
    """
    pool = charset_pool_size(password)
    if pool == 0:
        return 0.0

    charset_estimate = len(password) * math.log2(pool)
    distribution_estimate = shannon_entropy_per_symbol(password) * len(password)

    if distribution_estimate <= 0:
        return 0.0
    return min(charset_estimate, distribution_estimate)


def count_character_types(password: str) -> tuple[int, int, int, int, int]:
    lower = upper = digits = spaces = specials = 0
    for ch in password:
        if ch in string.ascii_lowercase:
            lower += 1
        elif ch in string.ascii_uppercase:
            upper += 1
        elif ch in string.digits:
            digits += 1
        elif ch == " ":
            spaces += 1
        else:
            specials += 1
    return lower, upper, digits, spaces, specials


def has_weak_sequence(password: str) -> bool:
    """True if password contains a short keyboard or alphabet run."""
    lowered = password.lower()
    for i in range(len(lowered) - 2):
        chunk = lowered[i : i + 3]
        for sequence in WEAK_SEQUENCES:
            if chunk in sequence:
                return True
    return False


def feedback_for_level(level: int, *, common: bool, weak_sequence: bool, has_spaces: bool) -> str:
    if common:
        return "Very weak — this password is commonly used. Choose something unique."
    if weak_sequence:
        return "Weak — avoid simple sequences (e.g. 123, abc, qwerty)."
    if has_spaces:
        return "Weak — spaces are often disallowed; try a longer password without spaces."
    messages = {
        0: "Enter a password to analyze.",
        1: "Very weak — increase length and character variety.",
        2: "Weak — add more character types and length.",
        3: "Fair — decent, but could be stronger.",
        4: "Good password.",
        5: "Excellent password.",
    }
    return messages.get(level, messages[1])


def level_from_entropy(entropy: float) -> int:
    if entropy < 28:
        return 1
    if entropy < 35:
        return 2
    if entropy < 50:
        return 3
    if entropy < 60:
        return 4
    return 5


def bar_style_for_level(level: int) -> str:
    if level <= 2:
        return "Red.Horizontal.TProgressbar"
    if level <= 3:
        return "Orange.Horizontal.TProgressbar"
    return "Green.Horizontal.TProgressbar"


def evaluate_password_strength(password: str) -> PasswordAnalysis:
    if not password:
        return PasswordAnalysis(
            report="Enter a password to see strength analysis.",
            level=0,
            progress=0,
            bar_style="Blue.Horizontal.TProgressbar",
        )

    lower, upper, digits, spaces, specials = count_character_types(password)
    entropy = estimate_entropy_bits(password)
    level = level_from_entropy(entropy)

    common = password.lower() in COMMON_PASSWORDS
    weak_sequence = has_weak_sequence(password)
    if common or weak_sequence or spaces > 0:
        level = min(level, 2 if (common or spaces > 0) else 3)

    feedback = feedback_for_level(
        level,
        common=common,
        weak_sequence=weak_sequence and not common,
        has_spaces=spaces > 0,
    )

    report = (
        f"Your password has:\n"
        f"{lower} lowercase letters\n"
        f"{upper} uppercase letters\n"
        f"{digits} digits\n"
        f"{spaces} spaces\n"
        f"{specials} special characters\n"
        f"Length: {len(password)}\n"
        f"Estimated entropy: {entropy:.2f} bits\n"
        f"Strength level: {level}/5\n"
        f"Remarks: {feedback}"
    )

    return PasswordAnalysis(
        report=report,
        level=level,
        progress=level * 20,
        bar_style=bar_style_for_level(level),
    )


def generate_password(length: int = 16, *, use_specials: bool = True) -> str:
    if length < 8:
        raise ValueError("Password length must be at least 8.")
    charset = string.ascii_letters + string.digits
    if use_specials:
        charset += SAFE_PUNCTUATION
    return "".join(secrets.choice(charset) for _ in range(length))
