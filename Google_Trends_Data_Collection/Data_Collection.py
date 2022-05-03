# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-26

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-30


from Database.Record import Record
from Google_Trends.Search import SearchEngine
from Google_Trends.URLs import Url
from csv import reader
from pytrends.exceptions import ResponseError
from termcolor import colored


def main():
    # Open the input CSV database.
    input_file = open(
        file=r"../Data_Cleanup/Output_File/Records.csv",
        mode='r',
        newline='',
        errors="ignore"
    )
    csv = reader(input_file)
    csv = list(csv)

    # Open the file storing the processed owner urls.
    owner_urls_file = open(
        file=r"../Google_Trends/Intermediate_File/Owner_URLs.txt",
        mode='r',
        errors="ignore"
    )

    # Open the file storing the common nicknames.
    nicknames_file = open(
        file=r"./Input_File/Nicknames.csv",
        mode='r',
        newline='',
        errors="ignore"
    )
    nicknames = reader(nicknames_file)
    nicknames = [[name for name in row if len(name) > 1 and ',' not in name] for row in list(nicknames)]

    # Open the file containing the starting index.
    start_file = open(
        file=r"../Google_Trends/Intermediate_File/Start.txt",
        mode='r',
        errors="ignore"
    )
    start = int(start_file.read())
    start_file.close()

    # Load the urls to a list.
    owner_urls = []

    lines_1 = owner_urls_file.readlines()
    for row in lines_1:
        if row.strip() == '':
            continue
        row = [row[:row.find(',')], row[row.find(',') + 1:]]
        url = Url(row[0])
        for num in row[1].split():
            url.push(int(num))
        owner_urls.append(url)
    owner_urls_file.close()

    # start = 2871
    end = len(csv)

    for i in range(start, end):
        record = Record(
            record_number=int(csv[i][0]),
            owner=csv[i][1],
            ticker=csv[i][2],
            cusip6=csv[i][3],
            cname=csv[i][4]
        )

        engine = SearchEngine()

        try:
            result_owner = engine.search_owner(record, owner_urls, nicknames)

            if result_owner is not None:
                output_file = open(
                    file=result_owner["dir"] + ("%05d_-_Owner_-_SVI_Data_-_CSV.csv" % record.get_record_number()),
                    mode='w',
                    errors="ignore"
                )
                output_file.write(result_owner["data"])
                output_file.close()

                print(colored(f"Owner of {record} Collected!", result_owner["color"]))
        except ResponseError:
            # Update the url files.
            owner_urls_file = open(
                file=r"../Google_Trends/Intermediate_File/Owner_URLs.txt",
                mode='w',
                errors="ignore"
            )
            for url in owner_urls:
                owner_urls_file.write("%s\n" % url)
            owner_urls_file.close()

            # Update the start file.
            start_file = open(
                file=r"../Google_Trends/Intermediate_File/Start.txt",
                mode='w',
                errors="ignore"
            )
            start_file.write(str(i))
            start_file.close()
            break

    # Close the input file.
    input_file.close()
    nicknames_file.close()


if __name__ == "__main__":
    main()
