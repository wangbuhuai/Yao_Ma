# Created by Dayu Wang (dwang@stchas.edu) on 2022-06-20

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-06-20


from csv import reader


RAW_OWNERS = "./Input_File/Input_File_-_Owners_-_CSV.csv"
PERSON_ID = "./Output_Files/Person_IDs_-_CSV.csv"

HEADERS = [
    "DATE",
    "OWNER",
    "PERSONID",
    "SVI_INDEX",
    "TICKER",
    "CUSIP6",
    "CNAME",
    "GOOGLE_TRENDS_SEARCH_TERM",
    "GOOGLE_TRENDS_SUGGESTION"
]


def main():
    # Open the input files.
    raw_owners_file = open(
        file=RAW_OWNERS,
        mode='r',
        newline='',
        errors="ignore"
    )
    person_id_file = open(
        file=PERSON_ID,
        mode='r',
        newline='',
        errors="ignore"
    )
    raw_owners = reader(raw_owners_file)
    ids = reader(person_id_file)

    # Open the output file.
    output_file = open(
        file="./Output_Files/Owners_with_Person_ID_-_CSV.csv",
        mode='w',
        errors="ignore"
    )
    output_file.write(','.join(HEADERS) + '\n')

    person_ids = dict()  # Use the dictionary to store person id.

    # Read all the person id and store them in the dictionary.
    skip_first_line = True
    for record in ids:
        if skip_first_line:
            skip_first_line = False
            continue
        person_ids[str(record[0]).strip().upper()] = str(record[1]).strip().upper()
    person_id_file.close()

    # Process the data in the input file.
    skip_first_line = True
    num = 2
    for record in raw_owners:
        if skip_first_line:
            skip_first_line = False
            continue

        record.insert(2, person_ids[str(record[1]).strip().upper()])
        output_file.write(','.join(record) + '\n')
        print("[%d] %s (%s) processed" % (num, record[1], record[2]))
        num += 1

    # Close the files.
    raw_owners_file.close()
    output_file.close()


if __name__ == "__main__":
    main()
