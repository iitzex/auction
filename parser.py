import requests
import re
from bs4 import BeautifulSoup


def find_table(addr):
    r = requests.get(addr)
    soup = BeautifulSoup(r.text, "html.parser")

    if soup.pre.pre is None:
        print("No Exist")
        return False

    context = soup.pre.pre.get_text().split('\n')

    table = []
    tag = False
    for line in context:
        if u'~T40X0L2;' in line:
            tag = True
            continue
        elif u'~T64X4L25;' in line:
            tag = False

        if tag:
            table.append(line)
    return table


def parse(table):
    owner = ''
    land = ''
    house = ''
    tag = ''
    for line in table:
        if line == u'┌─────────────────────────────────────────────────┐':
            tag = 'owner_start'
            print(tag)
        elif line == u'├─┬───────────────────────┬─┬─────┬──────┬────────┤' \
                or line == u'├─┬──┬───────┬───┬─────────────────┬────┬─────────┤':
            tag = 'owner_end'
            print(tag)
            parse_owner(owner.split('\n'))
            tag = ''
        elif line == u'├─┼───┼────┼───┼───┼──────┼─┼─────┼──────┼────────┤':
            tag = 'land_start'
            print(tag)
        elif line == u'├─┼───┼────┬───┬───┬──────┬─┬─────┬──────┬────────┤':
            tag = 'land_split'
            print(tag)
            parse_land(land.split('\n'))
            tag = 'land_start'
            land = ''
        elif line == u'└─┴───┴───────────────────────────────────────────┘' or \
                line == u'├─┴──┬┴───────────────────────────────────────────┤':
            tag = 'land_end'
            print(tag)
            parse_land(land.split('\n'))
            land = ''
        elif line == u'├─┼──┼───────┼───┼───────────┼─────┼────┼─────────┤':
            tag = 'house_start'
            print(tag)
        elif line == u'├─┼──┼───────┬───┬───────────┬─────┬────┬─────────┤' or \
                line == u'├─┴──┼────────────────────────────────────────────┤':
            tag = 'house_split'
            print(tag)
            parse_house(house.split('\n'))
            tag = 'house_start'
            house = ''
        elif line == u'└────┴────────────────────────────────────────────┘':
            tag = 'house_end'
            print(tag)
        else:
            if tag == 'owner_start':
                owner += line + '\n'
            if tag == 'land_start':
                land += line + '\n'
            if tag == 'house_start':
                house += line + '\n'


def parse_owner(context):
    token = (context[0]).split('：')
    owner = token[1].split(' ')[0]
    print(owner)


def parse_land(context):
    tag = ''
    land = [''] * 12
    comment = [''] * 10
    for line in context:
        if line == u'│  ├───┼────┴───┴───┴──────┴─┴─────┴──────┴────────┤':
            tag = 'land_slash'
            continue

        # detail
        if tag == '':
            for i, each in enumerate(line.split('│')):
                land[i] += each.strip()
        # comment
        else:
            for i, each in enumerate(line.split('│')):
                comment[i] += each.strip()

    print(land)
    print(comment)


def parse_house(context):
    house = [''] * 10
    comment = [''] * 7
    tag = ''
    for line in context:
        if line == u'│  ├──┼───────┴───┴───────────┴─────┴────┴─────────┤':
            tag = 'house_slash'
            continue

        # detail
        if tag == 'house_slash':
            for i, each in enumerate(line.split('│')):
                comment[i] += each.strip()
        else:
            for i, each in enumerate(line.split('│')):
                house[i] += each.strip()

    m = re.search('(.*)\-\-\-\-\-\-\-\-\-\-\-\-\-\-(.*)', house[3])
    land = m.group(1)
    house[3] = m.group(2)

    print(land)
    print(house)
    print(comment)


def parser(addr):
    table = find_table(addr)
    if table:
        parse(table)

if __name__ == '__main__':
    id = 'tpd/10508/08161831505.007' #character error
    id = 'tpd/10508/05161016415.020'
    id = 'tyd/10507/22091642010.010'
    id = 'tpd/10507/22102612486.033'

    addr = 'http://aomp.judicial.gov.tw/abbs/wkw/WHD2ASHOW.jsp?rowid=/' + id
    addr = 'http://aomp.judicial.gov.tw/abbs/wkw/WHD2ASHOW.jsp?rowid=%2Fild%2F10505%2F06082332902.002'
    parser(addr)
