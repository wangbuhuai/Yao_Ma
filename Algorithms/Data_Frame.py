# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-26

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-26


from Algorithms.Date import three_letter_month
from pandas import DataFrame
from re import search


def svi_reshape(svi_df):
    """ Formats the data frame of svi data returns from Google Trends
        :param svi_df: svi data
        :type svi_df: DataFrame
        :return: formatted svi data
        :rtype: str
    """
    result = "Year,Month,SVI Data\n"
    for row in svi_df.iterrows():
        result += "%4d," % row[0].year
        result += "%s," % three_letter_month(row[0].month)
        result += "%s\n" % row[1][0]

    return result
