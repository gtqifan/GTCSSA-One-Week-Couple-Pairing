import json
import random
import sys
import operator


def main():
    # read_path = sys.argv[0]
    read_path = 'input.json'
    data = []
    match = {}

    with open(read_path, 'r') as file:
        for line in file:
            if json.loads(line)['cp'] == '':
                data.append(json.loads(line))

    for i in range(0, len(data)):
        data[i]['match'] = {}

    # calculate match_rate for each pair of users
    for i in range(0, len(data)):
        p1 = data[i]
        p1_name = p1['name']
        for j in range(0, i):
            p2 = data[j]
            p2_name = p2['name']
            res = int((calculate(p1, p2) + calculate(p2, p1)) / 2)
            res = max(res, 0)
            p1['match'][p2_name] = res
            p2['match'][p1_name] = res
            match[(i, j)] = res

    # pair the users according to match_rate
    while match:
        tup, rate = max(match.items(), key=lambda x: x[1])
        if rate == 0:
            break
        i, j = tup
        p1 = data[i]
        p2 = data[j]
        p1['cp'] = p2['_openid']
        p1['cp_rate'] = rate
        p2['cp'] = p1['_openid']
        p2['cp_rate'] = rate
        p1['image_uploader'] = p1['name']
        p2['image_uploader'] = p1['name']
        p1['cp_name'] = p2['name']
        p2['cp_name'] = p1['name']

        # print(p1['name'], ' ', p1['cp_name'], rate)

        keys = list(match.keys())
        for key in keys:
            if i in list(key) or j in list(key):
                del match[key]

    file.close()

    with open('output.json', 'w') as file:
        for line in data:
            json.dump(line, file, indent=2, ensure_ascii=False)
    file.close()


# calculate match_rate between two users
def calculate(p1, p2):
    # the baseline score for pairing
    res = 10

    # if gender does not match, return 0
    if p1['expectedGender'] != p2['gender'] or p2['expectedGender'] != p1['gender']:
        return 0

    # compare height and weight. If two requirements matches +20, else -5
    if p2['height'] in range(int(p1['expectedHeightLowerBound']) - 5, int(p1['expectedHeightUpperBound']) + 5):
        res += 20
    elif int(p2['height']) >= int(p1['expectedHeightUpperBound']) + 5:
        res -= int(int(p2['height'] - (int(p1['expectedHeightUpperBound']) + 5)))
    else:
        res -= int(int(p1['expectedHeightLowerBound']) - int(p2['age']))

    if p2['weight'] in range(int(p1['expectedWeightLowerBound']) - 5, int(p1['expectedWeightUpperBound']) + 5):
        res += 20
    elif int(p2['weight']) >= int(p1['expectedWeightUpperBound']) + 5:
        res -= int(int(p2['weight'] - (int(p1['expectedWeightUpperBound']) + 5)))
    else:
        res -= int(int(p1['expectedWeightLowerBound']) - int(p2['age']))

    # compare age. if requirement matches +20 else -5
    if p2['age'] in range(int(p1['expectedAgeLowerBound']), int(p1['expectedAgeUpperBound'])):
        res += 20
    elif int(p2['age']) >= int(p1['expectedAgeUpperBound']):
        res -= (int(int(p2['age'] - int(p1['expectedAgeUpperBound'])))) * 5
    else:
        res -= (int(int(p1['expectedAgeLowerBound']) - int(p2['age']))) * 5

    # each unmatched merit -10
    if p1['expectedInterest'] is None:
        res += 30
    else:
        for interest in p2['interest']:
            if interest in p1['expectedInterest']:
                res += 10
            else:
                res -= 10

    # each matched characters +3
    for character in p2['character']:
        if character in p1['expectedCharacter']:
            res += 3

    # 上天の缘分 0-5 integer
    res += random.randint(0, 5)

    return res



if __name__ == "__main__":
    main()