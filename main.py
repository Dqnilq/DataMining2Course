from urllib.parse import urlparse
import numpy
from bs4 import BeautifulSoup
import requests
from graphviz import Digraph

DOMAIN = 'youtube.com'
HOST = 'http://' + DOMAIN
helping_map = []
dot = Digraph(comment='graph')
d = {}
FORBIDDEN_PREFIXES = ['#', 'tel:', 'mailto:']
links = set()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = requests.get(HOST, headers=headers)

def calc(matrix, v, e, n):
    for i in range(20):
        v = v.matrix_mult(matrix, v)
        v = 0.85 * v
        v = v + (1 - 0.85) / n * e
    return v


def mult_matrix_on_const(matrix, b):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            matrix[i][j] *= b
    return matrix


def mult_matrix_on_vector(matrix, vector):
    length = len(matrix)
    result = [0 for i in range(length)]
    for i in range(length):
        count = 0
        for j in range(length):
            count += vector[j] * matrix[i][j]
        result[i] = count
    return result


def sum_of_vectors(v1, v2):
    v3 = [0 for i in range(len(v1))]
    for i in range(len(v1)):
        count = v1[i] + v2[i]
        v3[i] = count
    return v3


def calc(matrix, v, e, n):
    trasponent_matrix(matrix)
    const = (1 - 0.85) / n
    matrix = mult_matrix_on_const(matrix, 0.85)
    b = [y * const for y in e]
    for i in range(20):
        v = mult_matrix_on_vector(matrix, v)
        v = sum_of_vectors(v, b)
    return v


def get_key(a, value):
    for k, v in a.items():
        if v == value:
            return k


def trasponent_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i < j:
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]


def add_all_links(depth, url, max_depth):
    if depth > max_depth:
        return
    links_to_handle_recursive = []
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.content, 'lxml')
    for tag_a in soup.find_all('a', href=lambda v: v is not None):
        link = tag_a['href']
        if all(not link.startswith(prefix) for prefix in
               FORBIDDEN_PREFIXES):
            if link.startswith('/') and not link.startswith('//'):
                link = HOST + link
            if urlparse(link).netloc == DOMAIN:
                if depth != max_depth:
                    if link not in links:
                        dot.node(str(len(links)), link)
                        dot.edge(str(get_key(d, url)), str(len(links)))
                        helping_map.append([get_key(d, url), len(d)])
                        d[len(links)] = link
                        links.add(link)
                        links_to_handle_recursive.append(link)
                    else:
                        dot.edge(str(get_key(d, url)), str(get_key(d, link)))
                        helping_map.append([get_key(d, url), get_key(d, link)])
                else:
                    if link in links:
                        dot.edge(str(get_key(d, url)), str(get_key(d, link)))
                        helping_map.append([get_key(d, url), get_key(d, link)])
    if depth < max_depth:
        for link in links_to_handle_recursive:
            add_all_links(depth + 1, link, max_depth=max_depth)


def links_traversal(root_url, max_depth):
    links.add(root_url)
    dot.node(str(0), root_url)
    d[0] = root_url
    add_all_links(0, root_url, max_depth=max_depth)


def creating_matrix_of_transitivity(a):
    count = 0
    for i in range(len(a)):
        if a[i][1] > count:
            count = a[i][1]
    count += 1
    matrix = [[0] * count for i in range(count)]
    outLinks = [0] * count
    for i in range(len(a)):
        matrix[a[i][0]][a[i][1]] += 1
        outLinks[a[i][0]] += 1
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if outLinks[i] != 0:
                matrix[i][j] /= outLinks[i]
    print('Transition Matrix:')
    f = open('TransitionMatrix.txt', 'w')
    for i in range(len(matrix)):
        print(*[matrix[i][j] for j in range(len(matrix))])
    print()
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    f.write(str('\n'.join(table)))
    f.close()
    return matrix


def sum_of_elements(v):
    sum = 0
    b = []
    f = open('pageRank.txt', 'w')
    for i in range(len(v)):
        b.append(v[i])
        sum += v[i]
    b.sort(reverse = True)
    for i in b:
        f.writelines(str(i) + "\n")
    f.close()
    return sum


def main():
    links_traversal(HOST + '/', 3)
    for link in links:
        print(link)
    print(dot.source)
    dot.render('C:\\Users\\Danila\\PycharmProjects\\pythonProject4\\graph', view=True)
    array = creating_matrix_of_transitivity(helping_map)
    v = [1 / len(links) for i in range(len(links))]
    e = [1 for i in range(len(links))]
    v = calc(array, v, e, len(links))
    print()
    print("Summary Page Rank:", toFixed(sum_of_elements(v), 5))
    rating = {}
    for i in range(len(v)):
        rating[d.get(i)] = v[i]
    list_it = list(rating.items())
    list_it.sort(key=lambda i: i[1], reverse=True)
    f = open('rate.txt', 'w')
    for i in list_it:
        f.write(str(i[0]) + ' : ' + str(i[1]) + '\n')
    f.write('\n' + "SUM = " + str(sum_of_elements(v)))
    f.close()


def toFixed(numObj, digits):
    return f"{numObj:.{digits}f}"


if __name__ == '__main__':
    main()
