# Created by Dayu Wang (dwang@stchas.edu) on 2022-07-07

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-07-07


from csv import reader


RAW_DATABASE = "C:/Users/wangb/OneDrive/Wang_Buhuai/OneDrive_Temp/Yao_Ma/Databases/Raw_Database_-_2022-03.csv"
INPUT_FILE = "./Output_Files/Output_File_-_Cnames_with_Cnums_-_CSV.csv"


def main():
    # Open the input file.
    input_file = open(
        file=INPUT_FILE,
        mode='r',
        newline='',
        errors="ignore"
    )
    raw = reader(input_file)

    data = dict()  # Using a dictionary to store the input data

    # Process the input data.
    skip_first_row = True
    for record in raw:
        if skip_first_row:
            skip_first_row = False
            continue

        date = str(record[0]).upper().strip()
        year = int(date[date.rfind('/') + 1:])
        month = int(date[:date.find('/')])
        cname = str(record[1]).upper().strip()
        cnum = str(record[2]).upper().strip()
        ticker = str(record[3]).upper().strip()
        cusip6 = str(record[4]).upper().strip()
        svi = int(str(record[-1]).upper().strip())

        # Add data to the dictionary.
        data[f"{cnum}-{year}-{month}"] = [date, cname, cnum, ticker, cusip6, svi, False]

    # Close the input file.
    input_file.close()

    # Open the raw 8M database.
    input_file = open(
        file=RAW_DATABASE,
        mode='r',
        newline='',
        errors="ignore"
    )
    raw = reader(input_file)

    # Process the records in the 8M raw database.
    skip_first_row = True
    trandate_index, cname_index, cnum_index, ticker_index, cusip6_index = None, None, None, None, None
    for record in raw:
        if skip_first_row:
            trandate_index = record.index("TRANDATE")
            cname_index = record.index("CNAME")
            cnum_index = record.index("CNUM")
            ticker_index = record.index("TICKER")
            cusip6_index = record.index("CUSIP6")
            skip_first_row = False
            continue

        date = str(record[trandate_index]).upper().strip()
        year = int(date[date.rfind('/') + 1:])
        month = int(date[:date.find('/')])
        cnum = str(record[cnum_index]).upper().strip()

        if f"{cnum}-{year}-{month}" in data:
            data[f"{cnum}-{year}-{month}"][1] = str(record[cname_index]).upper().strip()
            data[f"{cnum}-{year}-{month}"][3] = '' if str(record[ticker_index]).upper().strip() == '-' else str(record[ticker_index]).upper().strip()
            data[f"{cnum}-{year}-{month}"][4] = '' if str(record[cusip6_index]).upper().strip() == '-' else str(record[cusip6_index]).upper().strip()
            data[f"{cnum}-{year}-{month}"][-1] = True

    # Close the input file.
    input_file.close()

    # Open the output file.
    output_file = open(
        file="./Output_Files/Output_File_-_Cnum_Match_-_CSV.csv",
        mode='w',
        newline='',
        errors="ignore"
    )
    output_file.write(','.join([
        "DATE",
        "CNAME",
        "CNUM",
        "TICKER",
        "CUSIP6",
        "SVI_INDEX",
        "MATCHED"
    ]))
    output_file.write('\n')

    # Write the updated data to the output file.
    for value in data.values():
        output_file.write(','.join(['"' + str(item) + '"' for item in value]))
        output_file.write('\n')

    # Close the input and output file.
    output_file.close()


if __name__ == "__main__":
    main()
