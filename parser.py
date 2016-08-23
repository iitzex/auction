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
        elif line == u'├─┬─────────────────────┬─┬────┬────┬──────┬──────┤' \
                or line == u'├─┬──┬───────┬───┬─────────────────┬────┬─────────┤' \
                or line == u'├─┬───────────────────────┬─┬─────┬──────┬────────┤':
            tag = 'owner_end'
            print(tag)
            parse_owner(owner.split('\n'))
            tag = ''
        elif line == u'├─┼───┼────┼───┼───┼──────┼─┼─────┼──────┼────────┤' \
                or line == u'├─┼───┼────┼───┼───┼────┼─┼────┼────┼──────┼──────┤':
            tag = 'land_start'
            print(tag)
        elif line == u'├─┼───┼────┬───┬───┬──────┬─┬─────┬──────┬────────┤' \
                or line == u'├─┼───┼────┬───┬───┬────┬─┬────┬────┬──────┬──────┤':
            tag = 'land_split'
            print(tag)
            parse_land(land.split('\n'))
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
    m = re.search('.*財產所有人：(.*)', context[0])
    # print(m)
    owner = m.group(1)
    print(owner)


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


def parser(addr):
    table = find_table(addr)
    # for i in table:
    #     print(i)
    if table:
        parse(table)

if __name__ == '__main__':
    id = 'tpd/10508/08161831505.007' #character error
    id = 'tpd/10508/05161016415.020'
    id = 'tyd/10507/22091642010.010'
    id = 'tpd/10507/22102612486.033'

    addr = 'http://aomp.judicial.gov.tw/abbs/wkw/WHD2ASHOW.jsp?rowid=/' + id
    addr = 'http://aomp.judicial.gov.tw/abbs/wkw/WHD2ASHOW.jsp?rowid=%2Ftcd%2F10508%2F03111203609.014'
    print(addr)
    parser(addr)
