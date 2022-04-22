# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-13

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-21


from Google_Trends.Settings import PARAMETERS, SUGGESTIONS
from Google_Trends.Suggestion import match_suggestions
from pytrends.request import TrendReq
from re import sub


# A Google Trends search engine
class SearchEngine:
    # Constructor
    def __init__(self):
        """ Initializes a Google Trends search engine
            :return: None
        """
        self._start = PARAMETERS["Start_Date"]  # Start date of the search period
        self._end = PARAMETERS["End_Date"]  # End date of the search period
        self._hl = "en-US"  # Language
        self._tz = 360  # Timezone offset
        self._geo = "US"  # Geographic location
        self._suggestions = SUGGESTIONS is not None and len(SUGGESTIONS) != 0  # Whether to turn on suggestions
        self._term = []  # Search term
        self._url = None  # Url taken from the suggestions in Google Trends
        self._remote_suggestion = None  # Suggestion text taken from the suggestions in Google Trends
        self._remote_suggestion_term = None  # Search term under the matched suggestion in Google Trends
        self._reliable = False  # Indicates whether there is a suggestion match in Google Trends

    # Methods

    def get_term(self):
        """ Returns the search term
            :return: search term
            :rtype: str
        """
        return sub(r"[^A-Za-z ]", '', self._term[0])

    def set_term(self, term):
        """ Updates the search term
            :param term: updated term to search
            :type term: str
            :return: None
        """
        # Clear the current search terms.
        while len(self._term) > 0:
            self._term.pop()

        # Add the updated search term.
        self._term.append(term)

    def search(self):
        """ Search the term in Google Trends
            :return: search result
            :rtype: Pandas DataFrame
        """
        self._reliable = False

        # Initialize a search engine.
        engine = TrendReq(hl=self._hl, tz=self._tz)

        # Turn on suggestions if it is set.
        if self._suggestions:
            suggestions = match_suggestions(engine, self._term[0])

            if suggestions is not None:
                self._remote_suggestion_term = suggestions["term"]
                self._url = suggestions["url"]
                self._remote_suggestion = suggestions["suggestion"]
                self._reliable = True

        engine.build_payload(
            kw_list=[self._url] if self._url is not None else self._term,
            timeframe=self._start + ' ' + self._end,
            geo=self._geo
        )

        # Generate the search results.
        results = engine.interest_over_time()

        # If no SVI data is found, then return.
        if results.empty:
            return

        # Drop the data with little interest.
        results.drop(
            labels="isPartial",
            axis="columns",
            inplace=True
        )

        # Insert a column containing the search term.
        results.insert(
            loc=0,
            column="Owner",
            value=f"{self._term[0]}"
        )

        # Insert a column containing the Google Trends search term.
        results.insert(
            loc=1,
            column="Google Trends Search Term",
            value=f"{self._remote_suggestion_term}" if self._remote_suggestion_term is not None else "N/A"
        )

        # Insert a column containing the Google Trends suggestion.
        results.insert(
            loc=1,
            column="Google Trends Suggestion",
            value=f"{self._remote_suggestion}" if self._remote_suggestion is not None else "N/A"
        )

        # Change the date format to yyyy-mm.
        results.rename(
            lambda date: "%d-%02d" % (date.year, date.month),
            axis=0,
            inplace=True
        )

        # Change the last column's name to "SVI Index".
        results.rename(
            columns={results.keys()[-1]: "SVI Index"},
            inplace=True
        )

        return [results, self._reliable]
