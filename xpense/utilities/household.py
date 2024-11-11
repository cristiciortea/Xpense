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


def add_commas_to_number_text(text: str) -> str:
    # Split the text into parts before and after the first dot.
    parts = text.split('.', 1)
    before_dot = parts[0]
    after_dot = parts[1] if "." in text else ""

    # Add commas after every 3 characters in the part before the dot.
    comma_added = ','.join([before_dot[max(i - 3, 0):i] for i in range(len(before_dot), 0, -3)][::-1])

    # Reconstruct the text with the modified part before the dot.
    result = comma_added + ('.' + after_dot if "." in text else "")
    return result
