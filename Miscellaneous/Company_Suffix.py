# Created by Dayu Wang (dwang@stchas.edu) on 2022-05-05

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-05-05


from pandas import read_excel


def main():
    # Open the input file storing records.
    input_file = read_excel(
        io=r"../Output/Output_Files/Output_File_-_Owners_-_XLSX.xlsx",
        sheet_name="Output_SVI_Index_of_CEOs"
    )

    # Open the output file.
    output_file = open(
        file=r"Output_Files/Suffix.txt",
        mode='w',
        errors="ignore"
    )

    # Create a dictionary to store the suffix and frequency.
    freq = dict()

    # Create a set to store processed cname.
    cnames = set()

    # Read and process each cname in the input file.
    for _, row in input_file.iterrows():
        cname = str(row["CNAME"])

        if cname in cnames:
            continue

        suffix = cname.split()[-1].upper().strip()

        if suffix in freq:
            freq[suffix] += 1
        else:
            freq[suffix] = 1

        cnames.add(cname)

    # Sort the dictionary.
    freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

    # Write to the output file.
    for key, value in freq.items():
        output_file.write(f"{key} {value}\n")

    # Close the output file.
    output_file.close()


if __name__ == "__main__":
    main()
