# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-13

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-30


from Algorithms.Strings import name_match, one_token_match, reshape, two_token_match
from pytrends.request import TrendReq


OWNER_SUGGESTIONS = (
    "CEO",
    "Chief Executive Officer",
    "Executive"
    "Chairman",
    "Owner",
    "President",
    "Businessman",
    "Businessperson"
)

CNAME_SUGGESTIONS = (
    "Company",
    "Organization",
    "Corporation",
    "Corp",
    "LLC",
    "Co",
    "Cor",
    "Group",
    "Inc",
    "Ltd"
)


def match_name_suggestions(engine, term, nicknames):
    """ Matches a term with Google Trends suggestions
        :param engine: a Google Trends search engine
        :type engine: TrendReq
        :param term: local search term
        :type term: str
        :param nicknames: a dictionary of common nicknames
        :type nicknames: list
        :return: a dictionary containing the matched term and suggestion, or None if no matched suggestion found
        :rtype: dict
    """
    # Generate suggestions from Google Trends.
    remote_suggestions = engine.suggestions(term)

    for remote_suggestion in remote_suggestions:
        # Condition 1: search term must match.
        if name_match(term, remote_suggestion["title"], nicknames):
            # Condition 2: suggestion must match.
            for local_suggestion in OWNER_SUGGESTIONS:
                if local_suggestion.find(' ') == -1 and one_token_match(local_suggestion, remote_suggestion["type"]):
                    return {
                        "suggestion": reshape(remote_suggestion["type"]),
                        "term": reshape(remote_suggestion["title"]),
                        "url": remote_suggestion["mid"]
                    }
                if local_suggestion.find(' ') != -1 and two_token_match(local_suggestion, remote_suggestion["type"]):
                    return {
                        "suggestion": reshape(remote_suggestion["type"]),
                        "term": reshape(remote_suggestion["title"]),
                        "url": remote_suggestion["mid"]
                    }
