# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-24

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-24


from re import ASCII, IGNORECASE, search, sub


# Suffix of companies
COMPANY_SUFFIX = (
    "CO",
    "COR",
    "CORP",
    "GROUP",
    "INC",
    "LLC",
    "LTD"
)


class Record:
    """ A record in the input database. """

    # Constructor
    def __init__(self, record_number, owner, ticker, cusip6, cname):
        """ Constructs a Record object
            :param record_number: row index of the record in the input Excel database
            :type record_number: int
            :param owner: CEO of the organization
            :type owner: str
            :param ticker: ticker of the organization
            :type ticker: str
            :param cusip6: CUSIP6 value of the organization
            :type cusip6: str
            :param cname: name of the organization
            :type cname: str
            :return: None
        """
        # Data fields
        self._record_number = record_number
        self._owner = sub(r"\s+?", ' ', sub(r"[.,]", '', owner.strip()))
        self._ticker = '-' if str(ticker).strip() == "nan" else ticker.strip()
        self._cusip6 = '-' if str(cusip6).strip() == "nan" else cusip6.strip()
        self._cname = sub(r"\s+?", ' ', sub(r"[.,]", '', cname.strip()))

    # Getters

    def get_record_number(self):
        """ Returns the number of the record
            :return: number of the record
            :rtype: str
        """
        return self._record_number

    def get_owner(self):
        """ Returns the owner of the organization in the record
            :return: owner of the organization in the record
            :rtype: str
        """
        return self._owner

    def get_ticker(self):
        """ Returns the ticker of the organization in the record
            :return: ticker of the organization in the record
            :rtype: str
        """
        return self._ticker

    def get_cusip6(self):
        """ Returns the CUSIP6 value of the organization in the record
            :return: CUSIP6 value of the organization in the record
            :rtype: str
        """
        return self._cusip6

    def get_cname(self):
        """ Returns the name of the organization in the record
            :return: name of the organization in the record
            :rtype: str
        """
        return self._cname

    # Setters

    def set_record_number(self, record_number):
        """ Updates the number of the record
            :param record_number: updated value of the number of the record
            :type record_number: int
            :return: None
        """
        self._record_number = record_number

    def set_owner(self, owner):
        """ Updates the owner of the organization in the record
            :param owner: updated value of the owner of the organization in the record
            :type owner: str
            :return: None
        """
        self._owner = owner

    def set_ticker(self, ticker):
        """ Updates the ticker of the organization in the record
            :param ticker: updated value of the ticker of the organization in the record
            :type ticker: str
            :return: None
        """
        self._ticker = ticker

    def set_cusip6(self, cusip6):
        """ Updates the CUSIP6 value of the organization in the record
            :param cusip6: updated value of the CUSIP6 value of the organization in the record
            :type cusip6: str
            :return: None
        """
        self._cusip6 = cusip6

    def set_cname(self, cname):
        """ Updates the name of the organization in the record
            :param cname: updated value of the name of the organization in the record
            :type cname: str
            :return: None
        """
        self._cname = cname

    # Methods

    def __str__(self):
        """ Customizes the output format of the record
            :return: a string representing the output format of the record
            :rtype: str
        """
        return f"{{{self.get_record_number()}, " \
               f"{self.get_owner()}, " \
               f"{self.get_ticker()}, " \
               f"{self.get_cusip6()}, " \
               f"{self.get_cname()}}}"

    def check_owner(self):
        """ Tests whether the owner string is good for further processing
            :return: {True} if the owner string passes the test; {False} otherwise
            :rtype: bool
        """
        # If the record has neither ticker nor cusip6, then it fails the test.
        if self.get_ticker() == '-' and self.get_cusip6() == '-':
            return False

        # If the owner string contains non-English letter, then it fails the test.
        if search(r"[^\w\s\-.\']", self.get_owner(), ASCII) is not None:
            return False

        # If the owner is a company rather than a person, then it fails the test.
        for suffix in COMPANY_SUFFIX:
            # Generate the Python search regex.
            regex = r"\b"
            for index, ch in enumerate(suffix):
                regex += ch + r"\W*"
                if index != len(suffix) - 1:
                    regex += '?'
                else:
                    regex += '$'

            # Check whether there is a match for the regex.
            if search(regex, self.get_owner(), IGNORECASE) is not None:
                return False

        # Test passed if the above two cases are not satisfied
        return True
