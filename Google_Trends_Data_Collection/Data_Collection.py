# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-26

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-26


from Database.Record import Record
from Google_Trends.Search import SearchEngine
from Google_Trends.URLs import Url
from csv import reader


START = 19053
END = None


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

    # Open the file storing the processed urls.
    url_file = open(
        file=r"../Google_Trends/Intermediate_File/Processed_URLs.txt",
        mode='r',
        errors="ignore"
    )

    # Load the urls to a list.
    urls = []
    lines = url_file.readlines()
    for row in lines:
        if row.strip() == '':
            continue
        row = [row[:row.find(',')], row[row.find(',') + 1:]]
        url = Url(row[0])
        for num in row[1].split():
            url.push(int(num))
        urls.append(url)

    for i in range((1 if START is None else START), (len(csv) if END is None else END)):
        record = Record(
            record_number=int(csv[i][0]),
            owner=csv[i][1],
            ticker=csv[i][2],
            cusip6=csv[i][3],
            cname=csv[i][4]
        )

        engine = SearchEngine()

        try:
            result = engine.search_owner(record, urls)

            if result is not None:
                output_file = open(
                    file=result["dir"] + ("%05d_-_Owner_-_SVI_Data_-_CSV.csv" % record.get_record_number()),
                    mode='w',
                    errors="ignore"
                )
                output_file.write(result["data"])
                output_file.close()

                print(f"{record} Collected!")
        except:
            # Close the input files.
            input_file.close()
            url_file.close()

            # Update the url_file
            url_file = open(
                file=r"../Google_Trends/Intermediate_File/Processed_URLs.txt",
                mode='w',
                errors="ignore"
            )
            for url in urls:
                url_file.write("%s\n" % url)

            url_file.close()
            return

    # Close the input files.
    input_file.close()
    url_file.close()

    # Update the url_file
    url_file = open(
        file=r"../Google_Trends/Intermediate_File/Processed_URLs.txt",
        mode='w',
        errors="ignore"
    )

    for url in urls:
        url_file.write("%s\n" % url)

    url_file.close()


if __name__ == "__main__":
    main()
