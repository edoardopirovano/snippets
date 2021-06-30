import sys
import re


def parse_time(time):
    if "ms" in time:
        return int(re.search(r"^([0-9]+)ms$", time).group(1))
    if "m" in time:
        match = re.search(r"^([0-9]+)m([0-9]+)s$", time)
        minutes = int(match.group(1))
        seconds = int(match.group(2))
        return (1000 * 60 * minutes) + (1000 * seconds)
    if "s" in time and "." in time:
        match = re.search(r"^([0-9]+)\.([0-9]+)s$", time)
        seconds = int(match.group(1))
        decimal = int(match.group(2))
        return (1000 * seconds) + (100 * decimal)
    return int(re.search(r"^([0-9]+)s$", time).group(1)) * 1000


def read_timings(path):
    timings = {}
    with open(path, "r") as file:
        for line in file:
            if "Evaluation done" in line:
                time = parse_time(re.search(r"eval (.*?)\]", line).group(1))
                query = re.search(
                    r"writing results to (.*?)\.bqrs", line).group(1)
                timings[query] = time
    return timings


before = read_timings(sys.argv[1])
after = read_timings(sys.argv[2])
difference = {}
for query in after:
    if query in before:
        difference[query] = after[query] - before[query]

seen_positive = False
for query, change in sorted(difference.items(), key=lambda item: item[1]):
    if change > 0 and not seen_positive:
        print("---")
        print("(differences less than " + sys.argv[3] + " seconds omitted)")
        print("---")
        seen_positive = True
    if change > (int(sys.argv[3]) * 1000) or change < - (int(sys.argv[3]) * 1000):
        if change > 0:
            changeStr = "+" + str(change/1000) + " seconds"
        else:
            changeStr = str(change/1000) + " seconds"
        print(query + ".ql: " + changeStr)
