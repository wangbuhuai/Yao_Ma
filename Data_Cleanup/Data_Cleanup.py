# Created by Dayu Wang (dwang@stchas.edu) on 2022-04-24

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-04-26


from Database.Record import Record
from collections import deque
from pandas import read_excel


def main():
    # Open the input Excel database.
    input_file = read_excel(
        io=r"../Raw_Input_File/final_ceo_list.xlsx",
        sheet_name="search"
    )

    # Create the output CSV database.
    output_file = open("./Output_File/Records.csv", mode='w', errors="ignore")
    output_file.write("NUMBER,OWNER,TICKER,CUSIP6,CNAME\n")

    # Create two deques to store processed tickers and CUSIP6 values, respectively.
    tickers = deque()
    cusip6s = deque()

    # Process the rows in the input Excel database.
    for index, row in input_file.iterrows():
        # Create a record for the current row.
        record = Record(
            record_number=index + 2,
            owner=row["OWNER"],
            ticker=row["TICKER"],
            cusip6=row["CUSIP6"],
            cname=row["CNAME"]
        )

        # Skip the record if it has been processed (duplicate record).
        if record.get_ticker() != '-' and record.get_ticker() in tickers:
            continue
        if record.get_cusip6() != '-' and record.get_cusip6() in cusip6s:
            continue

        # Check the owner to see whether the record should be kept.
        if not record.check_owner():
            continue

        # Add the ticker and CUSIP6 of the record to the sets.
        if record.get_ticker() != '-':
            tickers.append(record.get_ticker())
            while len(tickers) > 10:
                tickers.popleft()
        if record.get_cusip6() != '-':
            cusip6s.append(record.get_cusip6())
            while len(cusip6s) > 10:
                cusip6s.popleft()

        # Write the record to the output file.
        output_file.write(f"{record.get_record_number()},"
                          f"{record.get_owner()},"
                          f"{record.get_ticker()},"
                          f"{record.get_cusip6()},"
                          f"{record.get_cname()}\n")

        # Print a message to the console.
        print(f"{record} Recorded!")


if __name__ == "__main__":
    main()
