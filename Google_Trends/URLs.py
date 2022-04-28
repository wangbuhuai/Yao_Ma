# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-26

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-28

from Algorithms.Files import move_to_manual_check


class Url:
    # Constructor
    def __init__(self, url):
        """ Constructs an Url object
            :param url: url used in Google Trends
            :type url: str
            :return: None
        """
        # Data fields
        self._url = url  # Stores the url used in Google Trends
        self._numbers = []  # Stores the record numbers related to the url

    # Getters

    def get_url(self):
        """ Returns the url in this object
            :return: url in this object
            :rtype: str
        """
        return self._url

    def get_numbers(self):
        """ Returns the record numbers related to this url
            :return: record numbers related to this url
            :rtype: list[int]
        """
        return self._numbers

    # Methods

    def push(self, record_number):
        """ Appends a record number to the rear end of the list storing the record numbers
            :param record_number: new record number to push
            :return: None
        """
        self._numbers.append(record_number)

    def __str__(self):
        """ Customizes the output format of the Url object
            :return: a string representing the output format
            :rtype: str
        """
        result = f"{self.get_url()}, "
        for num in self.get_numbers():
            result += f"{num} "
        return result


def url_check(url, record_number, urls, field):
    """ Checks whether the url has been processed earlier
        :param url: URL to check
        :type url: str
        :param record_number: record number of the url
        :type record_number: int
        :param urls: a list containing the urls processed
        :type urls: list[Url]
        :param field: either "Owner" or "Cname"
        :type field: str
        :return: {True} if the url has been processed earlier; {False} otherwise
        :rtype: bool
    """
    for i in range(len(urls)):
        if url == urls[i].get_url():
            if record_number in urls[i].get_numbers():
                return False
            else:
                # Move related files to "Need_Manual_Check" directory.
                move_to_manual_check(urls[i], field)

                urls[i].push(record_number)
                return True

    # Adds the new Url object.
    new_url = Url(url)
    new_url.push(record_number)
    urls.append(new_url)
    return False
