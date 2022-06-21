# Created by Dayu Wang (dwang@stchas.edu) on 2022-06-20

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-06-20


from csv import reader


OWNERS = "./Output_Files/Owners_with_Person_ID_-_CSV.csv"
DATABASE = "C:/Users/wangb/OneDrive/Wang_Buhuai/OneDrive_Temp/Yao_Ma/Databases/Raw_Database_-_2022-03.csv"


def main():
    # Open the owners file.
    owners_file = open(
        file=OWNERS,
        mode='r',
        newline='',
        errors="ignore"
    )
    owners = reader(owners_file)

    # Open the output file.
    output_file = open(
        file="./Output_Files/Output_-_Owners_-_CSV.csv",
        mode='w',
        errors="ignore"
    )

    queries = dict()  # Stores the queries in a dictionary.

    # Add key items to the dictionary.
    skip_first_row = True
    for record in owners:
        if skip_first_row:
            output_file.write(','.join(record) + ",TRANDATE\n")
            skip_first_row = False
            print(record)
            continue

        date = str(record[0]).strip().upper()
        year = int(date[date.rfind('/') + 1:])
        month = int(date[:date.find('/')])
        p_id = str(record[2]).strip().upper()

        queries["%s %d %d" % (p_id, year, month)] = record[:]
        while len(queries["%s %d %d" % (p_id, year, month)]) > 9:
            queries["%s %d %d" % (p_id, year, month)].pop(len(queries["%s %d %d" % (p_id, year, month)]) - 3)

    owners_file.close()

    # Open the raw database.
    database_file = open(
        file=DATABASE,
        mode='r',
        newline='',
        errors="ignore"
    )
    database = reader(database_file)

    # Iterate through the database.
    skip_first_row = True
    header = []
    for record in database:
        if skip_first_row:
            header = record
            skip_first_row = False
            continue

        p_id = str(record[header.index("PERSONID")]).strip().upper()
        owner = str(record[header.index("OWNER")]).strip().upper()
        ticker = str(record[header.index("TICKER")]).strip().upper()
        cusip6 = str(record[header.index("CUSIP6")]).strip().upper()
        cname = str(record[header.index("CNAME")]).strip().upper().replace(',', '')

        trandate = str(record[header.index("TRANDATE")]).strip().upper()
        year = int(trandate[trandate.rfind('/') + 1:])
        month = int(trandate[:trandate.find('/')])
        date = int(trandate[trandate.find('/') + 1:trandate.rfind('/')])

        key = "%s %d %d" % (p_id, year, month)
        if key in queries:
            queries[key][1] = owner
            queries[key][4] = ticker
            queries[key][5] = cusip6
            queries[key][6] = "\"%s\"" % cname
            output_file.write(','.join(queries[key]) + (",%d/%d/%d\n" % (month, date, year)))

    # Close the files.
    database_file.close()
    output_file.close()


if __name__ == "__main__":
    main()
