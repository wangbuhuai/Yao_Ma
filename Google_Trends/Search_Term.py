# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-19

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-19


from re import sub


class Record:
    # Constructor
    def __init__(self, row, owner, ticker, cusip6, cname):
        """ Constructs a Record object
            :param row: row number of the search term in the input Excel file
            :type row: int
            :param owner: owner of the organization
            :type owner: str
            :param ticker: ticker of the organization
            :type ticker: str
            :param cusip6: CUSIP6 of the organization
            :type cusip6: str
            :param cname: name of the organization
            :type cname: str
            :return: None
        """
        self._row = row
        self._owner = sub(r"[^A-Za-z ]", '', owner, count=len(owner))
        self._ticker = ticker
        self._cusip6 = cusip6
        self._cname = sub(r"[^A-Za-z ]", '', cname, count=len(cname))

    # Getters

    def get_row(self):
        """ Returns the Excel row number.
            :return: Excel row number
            :rtype: int
        """
        return self._row

    def get_owner(self):
        """ Returns the owner
            :return: owner
        """
        return self._owner

    def get_ticker(self):
        """ Returns the ticker
            :return: ticker
        """
        return self._ticker

    def get_cusip6(self):
        """ Returns the CUSIP6
            :return: CUSIP6
        """
        return self._cusip6

    def get_cname(self):
        """ Returns the cname
            :return: cname
        """
        return self._cname

    # Method

    def __str__(self):
        """ Customizes the output format
            :return: a string representing the output format of the object
        """
        return f"({self._row}, {self._owner})"
