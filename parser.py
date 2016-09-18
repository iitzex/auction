# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup


def find_table(addr):
    r = requests.get(addr)
    content = r.content.decode('Big5-HKSCS', errors='backslashreplace')

    if r.status_code != 200:
        print("Not Exist")
        return False

    soup = BeautifulSoup(content, "html.parser")
    context = soup.pre.pre.get_text().split('\n')

    table = []
    tag = False
    for line in context:
        if re.match('.*~T.*X.*;', line) and not tag:
            tag = True
            continue
        elif re.match('.*~T.*X.*;', line) and tag:
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
        elif line == u'├─┬─────────────────────┬─┬────┬────┬──────┬──────┤' \
                or line == u'├─┬──┬───────┬───┬─────────────────┬────┬─────────┤' \
                or line == u'├─┬───────────────────────┬─┬─────┬──────┬────────┤':
            tag = 'owner_end'
            print(tag)
            owner = parse_owner(owner.split('\n'))
            tag = ''
        elif line == u'├─┼───┼────┼───┼───┼──────┼─┼─────┼──────┼────────┤' \
                or line == u'├─┼───┼────┼───┼───┼────┼─┼────┼────┼──────┼──────┤':
            tag = 'land_start'
            print(tag)
        elif line == u'├─┼───┼────┬───┬───┬──────┬─┬─────┬──────┬────────┤' \
                or line == u'├─┼───┼────┬───┬───┬────┬─┬────┬────┬──────┬──────┤':
            tag = 'land_split'
            print(tag)
            land = parse_land(land.split('\n'))
            tag = 'land_start'
            land = ''
        elif line == u'└─┴───┴───────────────────────────────────────────┘' \
                or line == u'├─┴──┬┴───────────────────────────────────────────┤':
            tag = 'land_end'
            print(tag)
            parse_land(land.split('\n'))
            land = ''
        elif line == u'├─┼──┼───────┼───┼───────────┼─────┼────┼─────────┤' \
          or line == u'├─┼──┼───────┼───┼───────────┼─────┼──┼─────┼─────┤':
            tag = 'house_start'
            print(tag)
        elif line == u'├─┼──┼───────┬───┬───────────┬─────┬────┬─────────┤' \
                or line == u'├─┴──┼────────────────────────────────────────────┤' \
                or line == u'├─┼──┼───────┼───┼───────────┼─────┼──┼─────┼─────┤' \
                or line == u'├─┼──┼───────┬───┬───────────┬─────┬──┬─────┬─────┤':
            tag = 'house_split'
            print(tag)
            # print(house)
            parse_house(house.split('\n'))
            tag = 'house_start'
            house = ''
        elif line == u'└────┴────────────────────────────────────────────┘' \
                or line == u'└─┴──┴────────────────────────────────────────────┘':
            tag = 'house_end'
            print(tag)
            house = ''
        else:
            if tag == 'owner_start':
                owner += line + '\n'
            if tag == 'land_start':
                land += line + '\n'
            if tag == 'house_start':
                house += line + '\n'


def parse_owner(context):
    m = re.search('.*財產所有人：(.*).*│', context[0])
    owner = m.group(1).strip()

    print(owner)
    return owner


def parse_land(context):
    tag = ''
    land = [''] * 15
    comment = [''] * 12
    for line in context:
        if u'──' in line:
            tag = 'land_dash'
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
    return land


def parse_house(context):
    house = [''] * 15
    comment = [''] * 7
    tag = ''
    for line in context:
        if u'──' in line:
            tag = 'house_dash'
            continue

        # detail
        if tag == 'house_dash':
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
    return house


def parser(addr):
    table = find_table(addr)
    # for i in table:
    #     print(i)
    if table:
        parse(table)

if __name__ == '__main__':
    id = 'tpd/10508/08161831505.007' #character error
    id = 'tpd/10508/05161016415.020'
    id = 'tcd%2F10508%2F22100442180.034'

    addr = 'http://aomp.judicial.gov.tw/abbs/wkw/WHD2ASHOW.jsp?rowid=/' + id
    print(addr)
    parser(addr)
