# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-26

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-26


from re import ASCII, IGNORECASE, search, sub


def english_only(s):
    """ Tests whether a string has only English letters, digits, underscores, apostrophes, hyphens, and whitespaces
        :param s: string to test
        :type s: str
        :return: {True} if the string has only the mentioned characters; {False} otherwise
        :rtype: bool
    """
    return search(r"[^\w\s\-\']", s, ASCII) is None


def reshape(s):
    """ Formats a string for later use.
        :param s: string to format
        :type s: str
        :return: string after format
        :rtype: str
    """
    # Replace opening delimiters ('(', '[', and '{') with '('.
    s = sub(r"[(\[{]", '(', s, count=len(s))
    s = sub(r"(?<![(\s])\(", " (", s, count=len(s))

    # Replace closing delimiters (')', ']', and '}') with ')'.
    s = sub(r"[)\]}]", ')', s, count=len(s))
    s = sub(r"\)(?![)\s])", ") ", s, count=len(s))

    # Remove commas (',') and periods ('.').
    s = sub(r"[,.]", '', s, count=len(s))

    # Replace any whitespace (or combination of whitespaces) with a single space.
    s = sub(r"\s+?", ' ', s, count=len(s))

    # Return a trimmed string.
    return s.strip()


def remove_parentheses(s):
    """ Remove '(' and ')' characters from a string
        :param s: original string
        :type s: str
        :return: a copy of the original string with parentheses removed
        :rtype: str
    """
    return sub(r"[()]", '', s, count=len(s))


def two_token_match(local, remote):
    """ Tests whether there are at least two common tokens in two strings
        :param local: local string that has at least two tokens
        :type local: str
        :param remote: string from Google Trends that has at least two tokens
        :type remote: str
        :return: {True} if there are at least two common tokens in the two strings; {False} otherwise
        :rtype: bool
    """
    local = (remove_parentheses(token) for token in local.split())  # Split the local string into tokens.
    remote = remove_parentheses(reshape(remote))  # Format the remote string.
    count = 0  # Stores the number of matched tokens found

    for token in local:
        if search(fr"\b{token}\b", remote, IGNORECASE) is not None:
            count += 1
            if count == 2:
                return True

    return False


def one_token_match(local, remote):
    """ Tests whether a string appears entirely as a token in another string
        :param local: local string that has no spaces in it
        :type local: str
        :param remote: string from Google Trends
        :type remote: str
        :return: {True} if the local string appears entirely as a token in the remote string; {False} otherwise
        :rtype: bool
    """
    # Format the local and remote strings.
    local = remove_parentheses(local)
    remote = remove_parentheses(reshape(remote))

    return search(fr"\b{local}\b", remote, IGNORECASE) is not None
