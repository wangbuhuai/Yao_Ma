# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-13

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-13


from Google_Trends.Settings import SUGGESTIONS
from Google_Trends.Two_Token_Match import two_token_match
from pytrends.request import TrendReq


def match_suggestions(engine, term):
    """ Matches a term with Google Trends suggestions
        :param engine: a Google Trends search engine
        :type engine: TrendReq
        :param term: a Google Trends search term
        :type term: str
        :return: a dictionary containing the matched term and suggestion, or None if no matched suggestion found
        :rtype: Dict[str, str]
    """
    # Generate suggestions from Google Trends.
    remote_suggestions = engine.suggestions(term)

    for remote_suggestion in remote_suggestions:
        # Condition 1: search term must match.
        if two_token_match(term, remote_suggestion["title"]):
            # Condition 2: suggestion must match.
            for local_suggestion in SUGGESTIONS:
                if two_token_match(local_suggestion, remote_suggestion["type"]):
                    return {
                        "suggestion": remote_suggestion["type"],
                        "term": remote_suggestion["title"],
                        "url": remote_suggestion["mid"]
                    }
