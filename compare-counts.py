
import argparse
import subprocess
import json

parser = argparse.ArgumentParser(description='Compare two sets of tuple counts.')
parser.add_argument('--new',
                    help='the new structued log')
parser.add_argument('--main',
                    help='the structured log from main')
args = parser.parse_args()

tmpFolder = "/tmp"
mainSummary = tmpFolder + "/main.json"
newSummary = tmpFolder + "/new.json"
subprocess.call(["codeql", "generate", "log-summary", "--minify-output", args.new, newSummary])
subprocess.call(["codeql", "generate", "log-summary", "--minify-output", args.main, mainSummary])

def readCounts(summaryFile):
    allCounts = {}
    with open(summaryFile) as file:
        for line in file:
            predicateInfo = json.loads(line)
            if not "pipelineRuns" in predicateInfo:
                continue
            allCounts[predicateInfo["raHash"]] = predicateInfo["resultSize"]
    return allCounts

mainCounts = readCounts(mainSummary)
newCounts = readCounts(newSummary)

for predicate in mainCounts:
    if not predicate in newCounts:
        print("Predicate " + predicate + " is missing from the new log.")
        continue
    if mainCounts[predicate] != newCounts[predicate]:
        print("Predicate " + predicate + " has a different number of tuples in the new log.")