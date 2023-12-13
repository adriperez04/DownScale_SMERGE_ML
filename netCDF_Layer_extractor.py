import os
import fnmatch


def find_files(directory, extension):
    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, f'*.{extension}'):
            matches.append(os.path.join(root, filename))
    return matches


# Example usage:
if __name__ == "__main__":
    # Replace 'your_directory' with the path to the directory you want to search
    # Replace 'txt' with the file extension you're looking for
    search_directory = input("Enter the directory path to search: ")
    file_extension = input("Enter the file extension (without a dot): ")

    files = find_files(search_directory, file_extension)

    print(f"Found {len(files)} files with a .{file_extension} extension:")
    for file_path in files:
        print(file_path)
