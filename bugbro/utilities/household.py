def keep_first_dot(text: str) -> str:
    """Keeps the first dot in a string and removes all others.

    Args:
        text: The string to process.

    Returns:
        The string with only the first dot remaining, or the original string if no dots are found.
    """

    if "." not in text:
        return text

    # Find the index of the first dot.
    first_dot_index = text.index(".")

    # Replace all characters except the first dot with an empty string.
    return text[:first_dot_index + 1] + text[first_dot_index:].replace(".", "")
