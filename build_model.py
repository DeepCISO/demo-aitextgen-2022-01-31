import argparse
import numpy

from db.sqlite import get_sqlite_twint

parser = argparse.ArgumentParser(
    description="Fetches data from a number of sources and compiles a training set"
)
parser.add_argument(
    "--sqlite_twint", action="store", type=str, help="Where the bird site is stored"
)
args = parser.parse_args()

source_data = []
if args.sqlite_twint:
    temp = get_sqlite_twint(args.sqlite_twint)
    for item in temp:
        source_data.append(item)
    del temp

print("Compiling engagement data for each source user")
level_finder = {}
for item in source_data:
    if item["source"] == "twitter":
        key = item["source"] + "&" + item["author"]

    if key not in level_finder.keys():
        level_finder[key] = [item["score"]]
    else:
        temp = level_finder[key]
        temp.append(item["score"])
        level_finder[key] = temp

print("Computing engagement levels")
bars = {}
for key, dataset in level_finder.items():
    bars[key] = numpy.percentile(  # identify 85th percentile or lower posts
        level_finder[key], 85
    )

print("Filtering based on engagement level")
print("Pre:  " + str(len(source_data)))
filtered_data = []
for item in source_data:
    if item["source"] == "twitter":
        key = item["source"] + "&" + item["author"]
        bar = bars[key]

    if item["score"] >= bar:
        item["bar"] = bar
        filtered_data.append(item)
del source_data
print("Post: " + str(len(filtered_data)))

print("Removing cruft")
raw_content = []
for item in filtered_data:
    raw_content.append(item["content"])
del filtered_data

print("Processing content")
print("Pre:  " + str(len(raw_content)))
processed_content = []
for content in raw_content:
    content = content.lower()
    content = content.strip()
    # if adding reddit, this also needs to convert to all-text

    split_content = content.split()
    result_content = []
    seen_word = False
    for token in split_content:
        if not seen_word:
            if token.startswith("@"):
                continue
            else:
                seen_word = True

        if token.startswith("http://"):
            continue
        if token.startswith("https://"):
            continue

        result_content.append(token)

    if len(result_content) > 3:
        result = " ".join(result_content)
        processed_content.append(result)

print("Post: " + str(len(processed_content)))

with open("model.txt", "w") as file_obj:
    for line in processed_content:
        file_obj.write(line + "\r\n")
