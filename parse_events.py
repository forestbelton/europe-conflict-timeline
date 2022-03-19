import json
import operator
import re


def sort_events(events):
    sorted_events = sorted(events, key=lambda e: e["end"] - e["start"])
    return list(sorted(sorted_events, key=operator.itemgetter("start")))


def allocate_events(events):
    sorted_events = sort_events(events)
    reservations = {}
    allocations = [allocate_event(event, reservations) for event in sorted_events]
    return [
        {**event, "index": index} for event, index in zip(sorted_events, allocations)
    ]


def allocate_event(event, reservations):
    index = 0
    while True:
        reservations[index] = reservations.get(index, {})
        found = True
        for t in range(event["start"], event["end"] + 1):
            if t in reservations[index]:
                found = False
                break
        if found:
            for t in range(event["start"], event["end"] + 1):
                reservations[index][t] = 1
            break
        index += 1
    return index


PARSE_EVENT_RE = r"^(\d+)([–-](present|\d+))? (.*)"


def parse_event(raw_event: str):
    date_and_title = raw_event.split("\n")[0]
    match = re.match(PARSE_EVENT_RE, date_and_title)

    if match is None:
        raise Exception(f"invalid entry: '{raw_event}'")

    start = int(match.group(1))

    end = start
    if match.group(2):
        if match.group(2).endswith("present"):
            end = 2022
        else:
            end_str = match.group(2)[1:]
            if len(end_str) == 2 and start >= 1000:
                end = (start // 100) * 100 + int(end_str)
            else:
                end = int(end_str)

    return {
        "start": start,
        "end": end,
        "title": match.group(4),
    }


def valid_event(raw_event: str) -> bool:
    return "BC" not in raw_event and re.match(PARSE_EVENT_RE, raw_event) is not None


with open("raw_events.json", "r", encoding="utf-8") as f:
    raw_events = json.load(f)

parsed_events = [parse_event(event) for event in raw_events if valid_event(event)]
allocated_events = allocate_events(parsed_events)

with open("parsed_events.json", "w") as f:
    json.dump(sort_events(allocated_events), f)

with open("parsed_events.json", "r") as f:
    with open("parsed_events.js", "w") as g:
        g.write("const parsedEvents = ")
        g.write(f.read())
