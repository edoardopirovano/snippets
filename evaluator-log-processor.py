from ast import parse
import sys
import json
import dateutil.parser

def parseTime(time):
    return dateutil.parser.isoparse(time).timestamp()

for fileName in sys.argv[1:]:
    with open(fileName, 'r') as f:
        contents = f.read()

    predicatesInLayer = {}
    pipelineEndEvents = {}
    predicateStartEvents = {}

    log = list(map(json.loads, contents.split('\n\n')))
    for event in log:
        if 'predicateType' in event and event['predicateType'] == 'RECURSIVE_INTENSIONAL':
            layer = event['layerId']
            if layer not in predicatesInLayer:
                predicatesInLayer[layer] = []
            predicatesInLayer[layer].append(event['eventId'])
            predicateStartEvents[event['eventId']] = event
        if event['type'] == "PIPELINE_COMPLETED":
            pipelineEndEvents[event['startEvent']] = event
        if event['type'] == "LOG_HEADER":
            startTime = parseTime(event['time'])
        if event['type'] == "LOG_FOOTER":
            endTime = parseTime(event['time'])

    linearDuration = 0
    parallelDuration = 0
    for layer in predicatesInLayer:
        if len(predicatesInLayer[layer]) > 1:
            pipelineStartsInGeneration = {}
            for event in log:
                if event['type'] == "PIPELINE_STARTED" and event['predicateStartEvent'] in predicatesInLayer[layer]:
                    generation = event['generationNumber']
                    if generation not in pipelineStartsInGeneration:
                        pipelineStartsInGeneration[generation] = []
                    pipelineStartsInGeneration[generation].append(event)
            for generation in pipelineStartsInGeneration:
                canParallelise = True
                predicatesEvaluatedThisGeneration = []
                for event in pipelineStartsInGeneration[generation]:
                    startEvent = predicateStartEvents[event['predicateStartEvent']]
                    predicatesEvaluatedThisGeneration.append(startEvent['predicateName'])
                for event in pipelineStartsInGeneration[generation]:
                    startEvent = predicateStartEvents[event['predicateStartEvent']]
                    ra = startEvent['ra'][event['raReference']]
                    for line in ra:
                        if not canParallelise:
                            break
                        for predicate in predicatesEvaluatedThisGeneration:
                            if predicate + " " in line:
                                canParallelise = False
                                break
                if canParallelise:
                    maxDuration = 0
                    for startEvent in pipelineStartsInGeneration[generation]:
                        endEvent = pipelineEndEvents[startEvent['eventId']]
                        if startEvent['eventId'] == endEvent['startEvent']:
                            duration = parseTime(endEvent['time']) - parseTime(startEvent['time'])
                            if duration > maxDuration:
                                maxDuration = duration
                            linearDuration += duration
                    parallelDuration += maxDuration

    savings = linearDuration - parallelDuration
    totalTime = endTime - startTime
    percentageSavings = (savings / totalTime) * 100
    print(f"{fileName}: could save {savings:.1f} seconds out of {totalTime:.1f} ({percentageSavings:.1f}%)")
