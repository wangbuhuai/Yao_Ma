# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-13

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-13


from Google_Trends.Settings import PARAMETERS, SUGGESTIONS
from Google_Trends.Suggestion import match_suggestions
from pytrends.request import TrendReq


# A Google Trends search engine
class SearchEngine:
    # Constructor
    def __init__(self):
        """ Initializes a Google Trends search engine
            :return: None
        """
        self.start = PARAMETERS["Start_Date"]  # Start date of the search period
        self.end = PARAMETERS["End_Date"]  # End date of the search period
        self.hl = "en-US"  # Language
        self.tz = 360  # Timezone offset
        self.geo = "US"  # Geographic location
        self.suggestions = SUGGESTIONS is not None and len(SUGGESTIONS) != 0  # Whether to turn on suggestions
        self.term = []  # Search term
        self.url = None  # Url taken from the suggestions in Google Trends
        self.remote_suggestion = None  # Suggestion text taken from the suggestions in Google Trends

    # Methods

    def set_term(self, term):
        """ Updates the search term
            :param term: updated term to search
            :type term: str
            :return: None
        """
        # Clear the current search terms.
        while len(self.term) > 0:
            self.term.pop()

        # Add the updated search term.
        self.term.append(term)

    def search(self):
        """ Search the term in Google Trends
            :return: search result
            :rtype: Pandas DataFrame
        """
        # Initialize a search engine.
        engine = TrendReq(
            hl=self.hl,
            tz=self.tz,
        )

        # Turn on suggestions if it is set.
        if self.suggestions:
            suggestions = match_suggestions(engine, self.term[0])

            if suggestions is None:
                return

            self.set_term(suggestions["term"])
            self.url = suggestions["url"]
            self.remote_suggestion = suggestions["suggestion"]

        engine.build_payload(
            kw_list=[self.url] if self.url is not None else self.term,
            timeframe=self.start + ' ' + self.end,
            geo=self.geo
        )

        # Generate the search results.
        results = engine.interest_over_time()

        # Drop the data with little interest.
        results.drop(
            labels="isPartial",
            axis="columns",
            inplace=True
        )

        # Insert a column containing the search term.
        results.insert(
            loc=0,
            column="Name",
            value=f"{self.term[0]}\n({self.remote_suggestion})"
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

        return results
