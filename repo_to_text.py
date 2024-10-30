import os


def collect_text_files(src_dir, output_file):
    """
    Convert the repo to a single string
    :param src_dir:
    :param output_file:
    :return:
    """
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for dirpath, _, filenames in os.walk(src_dir):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)

                if filename.endswith('.txt') or filename.endswith('.py'):  # Adjust extensions as needed
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(f"+++++ {file_path} +++++\n")
                            outfile.write(infile.read() + "\n\n")
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")


if __name__ == "__main__":
    src_directory = "./src/"
    output_file = "./repo.txt"
    collect_text_files(src_directory, output_file)
