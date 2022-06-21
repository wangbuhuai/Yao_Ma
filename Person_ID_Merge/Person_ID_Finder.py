# Created by Dayu Wang (dwang@stchas.edu) on 2022-06-20

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-06-20


from csv import reader


RAW_OWNERS = "./Input_File/Input_File_-_Owners_-_CSV.csv"
RAW_DATABASE = "C:/Users/wangb/OneDrive/Wang_Buhuai/OneDrive_Temp/Yao_Ma/Databases/Raw_Database_-_2022-03.csv"


def main():
    # Open the raw database.
    raw_database_file = open(
        file=RAW_DATABASE,
        mode='r',
        newline='',
        errors="ignore"
    )
    raw_database = reader(raw_database_file)

    # Open the input file.
    raw_owners_file = open(
        file=RAW_OWNERS,
        mode='r',
        newline='',
        errors="ignore"
    )
    raw_owners = reader(raw_owners_file)

    # Open the output file.
    output_file = open(
        file="./Output_Files/Person_IDs_-_CSV.csv",
        mode='w',
        errors="ignore"
    )
    output_file.write("OWNER,PERSONID\n")

    owners = set()  # Stores the 917 owners.

    # Read the owners in the input file and store them in the set.
    skip_first_line = True
    for record in raw_owners:
        if skip_first_line:
            skip_first_line = False
            continue
        owner = str(record[1]).strip().upper()  # Extracts the owner.
        if owner not in owners:
            owners.add(owner)

    # Close the input file.
    raw_owners_file.close()

    processed = set()  # Stores the processed owners.

    # Iterate over the raw database.
    skip_first_line = True
    for record in raw_database:
        if skip_first_line:
            skip_first_line = False
            continue

        owner = str(record[6]).strip().upper()  # Extracts the owner.
        person_id = str(record[5]).strip().upper()  # Extracts the person id.

        if owner in processed or owner not in owners:
            continue

        output_file.write("%s,%s\n" % (owner, person_id))
        processed.add(owner)

        print("%03d) %s (%s) processed" % (len(processed), owner, person_id))

    # Close the files.
    raw_database_file.close()
    raw_owners_file.close()
    output_file.close()


if __name__ == "__main__":
    main()
