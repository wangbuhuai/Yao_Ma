# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-26

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-26


def three_letter_month(month):
    """ Returns the three-letter format of a month
        :param month: an integer representing a month (1 - 12)
        :type month: int
        :return: three-letter format of the month
        :rtype: str
    """
    if month == 1:
        return "Jan"
    if month == 2:
        return "Feb"
    if month == 3:
        return "Mar"
    if month == 4:
        return "Apr"
    if month == 5:
        return "May"
    if month == 6:
        return "Jun"
    if month == 7:
        return "Jul"
    if month == 8:
        return "Aug"
    if month == 9:
        return "Sep"
    if month == 10:
        return "Oct"
    if month == 11:
        return "Nov"
    if month == 12:
        return "Dec"
