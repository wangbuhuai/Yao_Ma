# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-26

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-30


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


def prepare(s):
    """ Formats a string for matching
        :param s: a string to format
        :return: formatted string
    """
    # Remove any token that has only one character.
    s = sub(r"\b\w\b", '', s, count=len(s))

    # Remove any parentheses from the string.
    s = sub(r"[()]", '', s, count=len(s))

    # Replace any whitespace (or combination of whitespaces) with a single space.
    s = sub(r"\s+?", ' ', s, count=len(s))

    # Return a trimmed string.
    return s.strip()


def two_token_match(local, remote):
    """ Tests whether there are at least two common tokens in two strings
        :param local: local string that has at least two tokens
        :type local: str
        :param remote: string from Google Trends that has at least two tokens
        :type remote: str
        :return: {True} if there are at least two common tokens in the two strings; {False} otherwise
        :rtype: bool
    """
    local = [token for token in prepare(local).split()]  # Split the local string into tokens.
    remote = prepare(reshape(remote))  # Format the remote string.
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
    local = prepare(local)
    remote = prepare(reshape(remote))

    return search(fr"\b{local}\b", remote, IGNORECASE) is not None


def name_match(local, remote, nicknames):
    """ Tests whether a name (local) matches another name (remote).
        :param local: a string of a full name in which the first token must be the last name
        :type local: str
        :param remote: a string of a full name
        :type remote: str
        :param nicknames: a dictionary of common nicknames
        :type nicknames: list
        :return: {True} if the two names match; {False} otherwise
        :rtype: bool
    """
    local = [token for token in prepare(local).split()]  # Split the local string into tokens.
    remote = prepare(reshape(remote))

    # Condition 1: last names must match.
    if search(fr"\b{local[0]}\b", remote, IGNORECASE) is not None:
        for i in range(1, len(local)):
            if search(fr"\b{local[i]}\b", remote, IGNORECASE) is not None:
                return True
            for row in nicknames:
                # Tests whether the token is in this row.
                for name in row:
                    if local[i].lower() == name.lower():
                        for token in row:
                            if search(fr"\b{token}\b", remote, IGNORECASE) is not None:
                                return True
                        break
    return False
