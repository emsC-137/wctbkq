from jisho_api.word import Word
import pandas as pd
import sys
from tqdm import tqdm
import glob
# %% Utils

def get_definition(word: str) -> str:
    r = Word.request(word)
    definition_str = ""
    sense_list = r.__dict__['data'][0].senses
    for defition_idx in range(len(sense_list)):
        definition_str = definition_str + str(defition_idx+1) + ". " + ", ".join(sense_list[defition_idx].english_definitions) + "\n"
    return definition_str

# %% Fuction

filename = "test_script.txt"

def to_cvs_table(filename: str) -> None:
    # Strip the txt file to turn it into csv table
    
    # Read the content of the file
    with open(filename, "r") as file:
        file_content = file.readlines()

    file_len = len(file_content)
    # Strip the line, add "," for csv format
    is_learnt = file_content[2].upper().isupper()
    for line_idx in range(file_len):
        if is_learnt:
            if line_idx % 3 != 2:
                file_content[line_idx] = file_content[line_idx].rstrip("\n") + ","
        else:
            if line_idx % 2 != 1:
                file_content[line_idx] = file_content[line_idx].rstrip("\n") + ","
    # Save the file
    with open(filename, "w") as file:
        for line in file_content:
            file.write(line)

def add_en_def(filename: str) -> None:
    # Added definition to the 'comment' column of the csv file

    df = pd.read_csv(filename, sep=",",header=None)
    # remove the 'review time' column from memrise
    df = df.drop(columns=[2], errors="ignore")
    
    # doing this the slow way for api
    comment_list = []
    for word in df[0].values:
        comment_list.append(get_definition(word))
    df['Comment'] = comment_list
    # fill in the other columns
    df['Instructions'] = "Type the reading!"
    df["Render as"] = "Image"
    df.columns = ["Question","Answers","Comment","Instructions","Render as"]

    df.to_csv(f'./csv/{filename[:-4]}.csv',index = False)

def main():
    args = sys.argv[1:]
    if not args:
        args = [f for f in glob.glob("*.txt")]
    for filename in args:
        print("Formating from txt to CSV file。。。\n")
        to_cvs_table(filename)
        print("Exporting to kotoba's format\n")
        add_en_def(filename)
        print(f"Finished for {filename}\n========\n")

if __name__ == "__main__":
    main()