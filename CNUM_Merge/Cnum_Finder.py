# Created by Dayu Wang (dwang@stchas.edu) on 2022-07-06

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-07-06


from csv import reader


RAW_CNAME = "./Input_File/Input_File_-_Cnames_-_CSV.csv"
RAW_DATABASE = "C:/Users/wangb/OneDrive/Wang_Buhuai/OneDrive_Temp/Yao_Ma/Databases/Raw_Database_-_2022-03.csv"


def main():
    input_file = open(
        file=RAW_CNAME,
        mode='r',
        newline='',
        errors="ignore"
    )
    raw_cnames = reader(input_file)

    records = set()

    skip_first_row = True
    for record in raw_cnames:
        if skip_first_row:
            skip_first_row = False
            continue
        records.add(str(record[2]).upper().strip())

    input_file.close()

    input_file = open(
        file=RAW_DATABASE,
        mode='r',
        newline='',
        errors="ignore"
    )
    raw_database = reader(input_file)

    output_file = open(
        file="./Output_Files/Output_File_-_CNUM_-_CSV.csv",
        mode='w',
        newline='',
        errors="ignore"
    )
    output_file.write("CNAME,CNUM\n")

    skip_first_row = True
    cnum_index = -1
    cname_index = -1
    for record in raw_database:
        if skip_first_row:
            cnum_index = record.index("CNUM")
            cname_index = record.index("CNAME")
            skip_first_row = False
            continue

        cnum = str(record[cnum_index]).upper().strip()
        cname = str(record[cname_index]).upper().strip()

        if cname in records:
            output_file.write("\"%s\",\"%s\"\n" % (cname, cnum))
            records.remove(cname)

    print(records)
    print(len(records))

    input_file.close()
    output_file.close()


if __name__ == "__main__":
    main()
