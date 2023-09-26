import json

with open('chart.json') as i:
    json_data = json.load(i)

for note in json_data['song']['notes']:
    for sectionNote in note['sectionNotes']:
        sectionNote[0] += 50

out_file = open("chartNew.json", "w")
json.dump(json_data, out_file, indent = 2)
out_file.close()