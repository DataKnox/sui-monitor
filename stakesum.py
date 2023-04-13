import json
f = open('stakes.json')
data = json.load(f)
f.close()
sum_prin = 0
for r in data['result']:
    for s in r['stakes']:
        sum_prin += s['principal']
print(sum_prin/1000000000)
