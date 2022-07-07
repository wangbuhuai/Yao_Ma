# Created by Dayu Wang (dwang@stchas.edu) on 2022-07-06

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-07-06


from csv import reader


CNAME = "./Input_File/Input_File_-_Cnames_-_CSV.csv"
CNUM = "./Output_Files/Output_File_-_CNUM_-_CSV.csv"


def main():
    input_1 = open(
        file=CNAME,
        mode='r',
        newline='',
        errors="ignore"
    )
    cnames = reader(input_1)

    input_2 = open(
        file=CNUM,
        mode='r',
        newline='',
        errors="ignore"
    )
    cnums = reader(input_2)

    output_file = open(
        file="./Output_Files/Output_File_-_Cnames_with_Cnums_-_CSV.csv",
        mode='w',
        newline='',
        errors="ignore"
    )
    output_file.write("DATE,CNAME,CNUM,TICKER,CUSIP6,SVI_INDEX\n")

    cnums_dict = dict()

    skip_first_row = True
    for record in cnums:
        if skip_first_row:
            skip_first_row = False
            continue
        cnums_dict[str(record[0]).upper().strip()] = str(record[1]).upper().strip()

    skip_first_row = True
    for record in cnames:
        if skip_first_row:
            skip_first_row = False
            continue

        date = str(record[1]).upper().strip()
        cname = str(record[2]).upper().strip()
        if cname not in cnums_dict:
            continue
        cnum = cnums_dict[cname]
        ticker = '' if str(record[3]).upper().strip() == '-' else str(record[3]).upper().strip()
        cusip6 = '' if str(record[4]).upper().strip() == '-' else str(record[4]).upper().strip()
        svi = str(record[5]).upper().strip()

        output_file.write("\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"\n" % (date, cname, cnum, ticker, cusip6, svi))

    input_1.close()
    input_2.close()
    output_file.close()


if __name__ == "__main__":
    main()
