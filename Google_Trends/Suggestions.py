# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-13

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-26


from Algorithms.Strings import one_token_match, two_token_match
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


def match_suggestions(engine, term, field):
    """ Matches a term with Google Trends suggestions
        :param engine: a Google Trends search engine
        :type engine: TrendReq
        :param term: local search term
        :type term: str
        :param field: "Owner" or "Cname"
        :type field: str
        :return: a dictionary containing the matched term and suggestion, or None if no matched suggestion found
        :rtype: dict
    """
    # Generate suggestions from Google Trends.
    remote_suggestions = engine.suggestions(term)

    for remote_suggestion in remote_suggestions:
        # Condition 1: search term must match.
        if two_token_match(term, remote_suggestion["title"]):
            # Condition 2: suggestion must match.
            for local_suggestion in (OWNER_SUGGESTIONS if field == "Owner" else CNAME_SUGGESTIONS):
                if local_suggestion.find(' ') == -1 and one_token_match(local_suggestion, remote_suggestion["type"]):
                    return {
                        "suggestion": remote_suggestion["type"],
                        "term": remote_suggestion["title"],
                        "url": remote_suggestion["mid"]
                    }
                if local_suggestion.find(' ') != -1 and two_token_match(local_suggestion, remote_suggestion["type"]):
                    return {
                        "suggestion": remote_suggestion["type"],
                        "term": remote_suggestion["title"],
                        "url": remote_suggestion["mid"]
                    }
