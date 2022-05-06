# Created by Dayu Wang (dwang@stchas.edu) on 2022-05-05

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-05-05


from csv import reader


def main():
    # Open the input file storing records.
    input_file = open(
        file=r"../Data_Cleanup/Output_File/Records.csv",
        mode='r',
        newline='',
        errors="ignore"
    )
    csv = reader(input_file)
    csv = list(csv)

    # Open the output file.
    output_file = open(
        file=r"Output_Files/Suffix.txt",
        mode='w',
        errors="ignore"
    )

    # Create a dictionary to store the suffix and frequency.
    freq = dict()

    # Read and process each cname in the input file.
    for row in range(1, len(csv)):
        cname = str(csv[row][4])
        suffix = cname.split()[-1].upper().strip()

        if suffix in freq:
            freq[suffix] += 1
        else:
            freq[suffix] = 1

    # Sort the dictionary.
    freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

    # Write to the output file.
    for key, value in freq.items():
        output_file.write(f"{key} {value}\n")

    # Close the input and output file.
    input_file.close()
    output_file.close()


if __name__ == "__main__":
    main()
