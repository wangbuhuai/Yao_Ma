# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-13

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-15


from re import IGNORECASE, search, sub


def two_token_match(pattern, text):
    """ Checks whether at least two tokens in a string matches the tokens in another string
        :param pattern: pattern to match in the text
        :type pattern: str 
        :param text: text to search for the pattern
        :type text: str
        :return: {True} if at least two tokens in the pattern appear in the text; {False} otherwise
        :rtype: bool
    """
    tokens = pattern.split()
    count = 0  # Counter of matched tokens
    for token in tokens:
        token = sub(r"[^A-Za-z]", '', token, count=len(token))
        if len(token) > 1 and search(f"\\b{token}\\b", text, IGNORECASE) is not None:
            count += 1
            if count == 2:
                return True
    return False
