import csv
import itertools
import tabulate


# here we are transforming our list from char to int value
def buckTrans(buckets, pairs, mapping):
    for a in buckets.values():
        key = getKey(buckets, a)
        line = a.split(',')
        for b in line:
            line[line.index(b)] = mapping[b]
        if len(line) > 1:
            pairs[key] = list(itertools.combinations(line, 2))


# singletone filter
def singlFill(row, singletons):
    if list(row)[3] not in singletons.keys():
        singletons[list(row)[3]] = 1
    else:
        singletons[list(row)[3]] += 1

# bucket filter
def buckFill(row, buckets):
    if list(row)[2] not in buckets.keys():
        buckets[list(row)[2]] = str(list(row)[3])
    else:
        s = buckets[list(row)[2]]
        if list(row)[3] not in s.split(','):
            s += ',' + list(row)[3]
            buckets[list(row)[2]] = s



# trying to itent
def identification(row, mapping, count):
    if list(row)[3] not in mapping.keys():
        mapping[list(row)[3]] = count
        count += 1
    return count


def MultiAlg():
    with open('dataset.csv', 'r', newline='') as csv_file:
        buckets = {}
        singletons = {}
        mapping = {}
        pairs = {}
        count = 1
        result = []
        spam_reader = csv.reader(csv_file)
        for row in spam_reader:
            count = identification(row, mapping, count)
            singlFill(row, singletons)
            buckFill(row, buckets)
        support_threshold = sum(singletons.values()) / len(singletons.values())
        buckTrans(buckets, pairs, mapping)
        hash_buckets1 = {}
        hashing_util = {}
        second_hashing_buckets = {}
        pairs_count = {}
        for a in pairs.values():
            count = 0
            key = getKey(pairs, a)
            for b in a:
                hash = (b[0] + b[1]) % len(mapping)
                if hash not in hash_buckets1.keys():
                    hash_buckets1[hash] = [1, 0]
                else:
                    hash_buckets1[hash][0] += 1
                hash2 = (b[0] + 2 * b[1]) % len(mapping)
                if hash2 not in hashing_util.keys():
                    hashing_util[hash2] = [1, 0]
                else:
                    hashing_util[hash2][0] += 1
                if hashing_util[hash2][0] > support_threshold:
                    hashing_util[hash2][1] = 1
                pairs[key][count] = hash
                count += 1
                if hash_buckets1[hash][0] > support_threshold:
                    hash_buckets1[hash][1] = 1
                    second_hashing_buckets[hash2] = hashing_util[hash2]
                if b not in pairs_count.keys():
                    pairs_count[b] = [hash, hash2]
        for a in pairs_count.keys():
            if hash_buckets1[pairs_count[a][0]][1] == 1 and singletons[getKey(mapping, a[0])] > support_threshold \
                    and singletons[getKey(mapping, a[1])] > support_threshold:
                if pairs_count[a][1] in second_hashing_buckets.keys():
                    if second_hashing_buckets[pairs_count[a][1]][1] == 1:
                        result.append('(' + getKey(mapping, a[0]) + ', ' + getKey(mapping, a[1]) + ')')
        for b in singletons.keys():
            if singletons[b] > support_threshold:
                result.append(b)
        return result


def getKey(d, value):
    for k, v in d.items():
        if v == value:
            return k


if __name__ == '__main__':
    f = open('result.txt', 'w')
    a = MultiAlg()
    for b in a:
        f.write(b + '\n')
    f.close()
