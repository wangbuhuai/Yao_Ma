# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-13

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-28


from Algorithms.Data_Frame import svi_reshape
from Database.Record import Record
from Google_Trends.Suggestions import match_suggestions
from Google_Trends.URLs import Url, url_check
from pytrends.request import TrendReq


# A Google Trends search engine
class SearchEngine:
    # Constructor
    def __init__(self):
        """ Initializes a Google Trends search engine
            :return: None
        """
        # Data fields
        self._engine = TrendReq(
            hl="en-US",  # Language
            tz=360  # Timezone offset
        )  # A Google Trends search engine

    # Methods

    def search_owner(self, record, urls):
        """ Searches the owner of the organization in a record on Google Trends
            :param record: a record in the input CSV database
            :type record: Record
            :param urls: a list containing the urls processed
            :type urls: list[Url]
            :return: a dictionary containing the search result and whether the result is reliable
            :rtype: dict
        """
        # Define some entities for later use.
        remote_suggestion_term = None  # Stores the term for the matched remote suggestion
        remote_suggestion = None  # Stores the matched remote suggestion
        url = None  # Stores the url if suggestion found
        output_directory = r"../Google_Trends_Data_Collection/Output_Files/Owner/"  # Directory to store the output file
        category = "Unreliable"  # Stores the category of the record

        # Try to match suggestions on Google Trends.
        suggestions = match_suggestions(self._engine, record.get_owner(), "Owner")
        if suggestions is not None:
            remote_suggestion_term = suggestions["term"]
            remote_suggestion = suggestions["suggestion"]
            url = suggestions["url"]

            # Check whether the url has been processed earlier.
            if url_check(url, record.get_record_number(), urls, "Owner"):
                output_directory += r"Need_Manual_Check/"
                category = "Manual Check"
            else:
                output_directory += "Reliable/"
                category = "Reliable"

        if url is None:
            output_directory += "Unreliable/"

        self._engine.build_payload(
            kw_list=[url] if url is not None else [record.get_owner()],
            timeframe="2004-01-01" + ' ' + "2022-03-31",  # Search time period
            geo="US"  # Search geographic location
        )

        results = self._engine.interest_over_time()  # Generate search results.

        # If no SVI data is found, then return.
        if results.empty:
            return

        # Add the output file header.
        output_data = f"Owner:,{record.get_owner()}\n" \
                      f"Cname:,{record.get_cname()}\n" \
                      f"Google Trends Search Term:,{remote_suggestion_term}\n" \
                      f"Google Trends Suggestion:,{remote_suggestion}\n" \
                      f"Category:,{category}\n\n"

        # Reshape the SVI data.
        output_data += svi_reshape(results)

        return {
            "dir": output_directory,
            "data": output_data
        }

    def search_cname(self, record, urls):
        """ Searches the name of the organization in a record on Google Trends
            :param record: a record in the input CSV database
            :type record: Record
            :param urls: a list containing the urls processed
            :type urls: list[Url]
            :return: a dictionary containing the search result and whether the result is reliable
            :rtype: dict
        """
        # Define some entities for later use.
        remote_suggestion_term = None  # Stores the term for the matched remote suggestion
        remote_suggestion = None  # Stores the matched remote suggestion
        url = None  # Stores the url if suggestion found
        output_directory = r"../Google_Trends_Data_Collection/Output_Files/Cname/"  # Directory of the output file
        category = "Unreliable"  # Stores the category of the record

        # Try to match suggestions on Google Trends.
        suggestions = match_suggestions(self._engine, record.get_cname(), "Cname")
        if suggestions is not None:
            remote_suggestion_term = suggestions["term"]
            remote_suggestion = suggestions["suggestion"]
            url = suggestions["url"]

            # Check whether the url has been processed earlier.
            if url_check(url, record.get_record_number(), urls, "Cname"):
                output_directory += r"Need_Manual_Check/"
                category = "Manual Check"
            else:
                output_directory += "Reliable/"
                category = "Reliable"

        if url is None:
            output_directory += "Unreliable/"

        self._engine.build_payload(
            kw_list=[url] if url is not None else [record.get_cname()],
            timeframe="2004-01-01" + ' ' + "2022-03-31",  # Search time period
            geo="US"  # Search geographic location
        )

        results = self._engine.interest_over_time()  # Generate search results.

        # If no SVI data is found, then return.
        if results.empty:
            return

        # Add the output file header.
        output_data = f"Cname:,{record.get_cname()}\n" \
                      f"Owner:,{record.get_owner()}\n" \
                      f"Google Trends Search Term:,{remote_suggestion_term}\n" \
                      f"Google Trends Suggestion:,{remote_suggestion}\n" \
                      f"Category:,{category}\n\n"

        # Reshape the SVI data.
        output_data += svi_reshape(results)

        return {
            "dir": output_directory,
            "data": output_data
        }
