import re
from pathlib import Path
import argparse

class MBDGDict(object):
    def __init__(self, dict_file_path = "mbdg-dict.txt"):
        self.dict_file_path = dict_file_path
        self.dictionary = {}
        self._parse_dictionary(dict_file_path)

    def _parse_dictionary(self, dict_file_path):
        self.dictionary = {}
        m = re.compile(r'(.*?) (.*?) \[(.*?)\] \/(.*)/$')
        with open(self.dict_file_path, "r") as f:
            for line in f:
                if line[0] == "#":
                    continue
                match = m.match(line)
                try:
                    simplified_entry = match.group(2)
                    entry = {"simp": simplified_entry,
                        "trad": match.group(1),
                        "pron": match.group(3),
                        "defs": match.group(4).split("/")}
                    self.dictionary[simplified_entry] = entry
                except AttributeError:
                    print(line, " - does not conform to format")
    
    def single_lookup(self, entry):
        if entry in self.dictionary.keys():
            return self.dictionary[entry]
        else:
            return None

    def single_formatted_lookup(self, entry):
        res = self.single_lookup(entry)
        if res is None:
            out = f"Entry '{entry}' is not found. Please try again."
        else:
            out = f"{res['simp']} {res['pron']} {str(res['defs'])}\n"
        return out

    def bulk_lookup(self, lookup_file_path, output_file_path=None, mode="simplified"):
        if mode != "simplified":
            raise NotImplementedError
        if output_file_path is None:
            path =  Path(lookup_file_path)
            output_file_path = str(path.with_suffix("")) + "_lookup" + path.suffix

        with open(output_file_path, "a+") as w:
            with open(lookup_file_path, "r") as f: 
                for line in f:
                    line = line.strip()
                    out = self.single_formatted_lookup(line)
                    w.write(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--lookup", help="Usage: python parse-mbdg.py --lookup <file_to_lookup> [-o output_file_path] \n"
                                    "Given a text file of words to look up, provivides the dictionary entries"
                                    "for those words.", type=str)
    parser.add_argument("-o", "--output", help="Usage: python parse-mbdg.py --lookup <file_to_lookup> [-o output_file_path] \n"
                                    "Output path to save the looked up entries. Default is lookup file name prefix + '_lookup' + suffix", type=str)
    parser.add_argument("-dd", "--dictionary", help="Path to dictionary file. Default: './mbdg-dict.txt'", type=str)
    parser.add_argument("-w", "--word", help="Word to Look Up.", type=str)

    args = parser.parse_args()
    
    dict_path = "mbdg-dict.txt"
    if args.dictionary:
        dict_path = args.dictionary
    dictionary = MBDGDict(dict_path)

    if args.word:
        entry = args.word.strip()
        print(dictionary.single_formatted_lookup(entry))
        exit(0)

    if args.lookup:
        if args.output:
            output_file_path = args.output
        else:
            output_file_path = None
        dictionary.bulk_lookup(args.lookup, output_file_path=output_file_path)
        exit(0)

    while True:
        entry = input("> Please input a dictionary entry to look up [Q to quit]:\n")
        if entry == "Q":
            exit(0)
        print(dictionary.single_formatted_lookup(entry))

