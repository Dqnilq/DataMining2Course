import hashlib
import vk_api
from math import log
import requests

def postParser():
    vk_session = vk_api.VkApi('+79510643152', '12obeziv')
    vk_session.auth()
    vk = vk_session.get_api()
    Count = 1
    posts = vk.wall.get(domain='itis_kfu', count=1)
    post_list = []
    i = 0
    f = open('text.txt', 'w', encoding='UTF-8')
    while i < Count:
        filtered_posts = posts['items'][i]['text']
        post_list.append(filtered_posts)
        i += 1
    words = []
    for post in post_list:
        words = post.split()
    for word in words:
        f.write(word)
        f.write('\n')
    f.close()
    return words

def bloomFilter(k, obj, n):
    bloom_filter = listOfZeros(n)
    for object in obj:
        count = 0

        index = int((hashlib.sha3_512(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.blake2s(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.shake_128(object.encode('utf-8')).hexdigest(56)), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.sha1(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.sha512(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.sha224(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.sha384(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.md5(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.sha3_224(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.sha3_256(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.blake2b(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.shake_256(object.encode('utf-8')).hexdigest(56)), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.sha256(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue

        index = int((hashlib.sha3_384(object.encode('utf-8')).hexdigest()), 16) % n
        bloom_filter[index] += 1
        count += 1
        if count == k:
            continue
    return bloom_filter



def checkWords(words, bloom_filter, count_of_hashes):
    for word in words:
        words_util = [word]
        new_bloomEx = bloomFilter(count_of_hashes, words_util, len(bloom_filter))
        count = 0
        for a in new_bloomEx:
            if a == 1:
                index = new_bloomEx.index(a)
                new_bloomEx[index] = 0
                if bloom_filter[index] > 0:
                    count += 1
        if count == count_of_hashes:
            print(word + ' - the word is, the probability of erroneous detection = ' + str("%.5f" % (0.5 ** count_of_hashes)))
        else:
            print(word + ' - no word')

s = ['Институт', 'данные', 'обучение', 'форма', 'завтра', 'спорт', 'организация', 'ИТИС', 'учеба', 'ДУ']


def listOfZeros(size):
    list_of_zeros = [0] * size
    return list_of_zeros



if __name__ == '__main__':
    precision = 0.0001
    words = postParser()
    m = len(words)
    n = int(log(precision) / log(0.5 ** (log(2) / m)))
    k = n / m * log(2)
    if k.is_integer():
        k = int(n / m * log(2))
    else:
        k = int(n / m * log(2)) + 1
    bloomEx = bloomFilter(k, words, n)
    checkWords(s, bloomEx, k)