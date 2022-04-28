# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-26

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-26


from os import listdir
from os.path import isfile, join
from shutil import move


def move_to_manual_check(url):
    """ Moves the files related to an url from "Reliable" directory to "Need_Manual_Check" directory
        :param url: related Url object
        :type: Url
        :return: None
    """
    directory = r"../Google_Trends_Data_Collection/Output_Files/Reliable"
    for filename in listdir(directory):
        file = join(directory, filename)
        if isfile(file) and int(filename[:5]) in url.get_numbers():
            move(file, r"../Google_Trends_Data_Collection/Output_Files/Need_Manual_Check")
