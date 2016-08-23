import requests
from bs4 import BeautifulSoup
from parser import parser


def traverse(court, proptype, saletype, key):
    addr = "http://aomp.judicial.gov.tw/abbs/wkw/WHD2A03.jsp?" + \
            key + \
           "&hsimun=all&ctmd=all&sec=all&saledate1=&saledate2=&crmyy=&crmid=&crmno=&" + \
           "dpt=&minprice1=&minprice2=&saleno=&area1=&area2=&registeno=&checkyn=all&" + \
           "emptyyn=all&rrange=不分&comm_yn=&owner1=&order=odcrm&" + \
           "courtX=" + court + "&proptypeX=" + proptype + "&saletypeX=" + saletype + \
           "&pageTotal=13&pageSize=15&rowStart=11&query_typeX=db&"

    r = requests.get(addr)
    soup = BeautifulSoup(r.text, "html.parser")
    pageTotal = soup.input['value']
    print('pageTotal:' + pageTotal)

    page = 1
    while page <= int(pageTotal):
        link = addr + "pageNow=" + str(page)
        print(link)
        r = requests.get(link)
        soup = BeautifulSoup(r.text, "html.parser")
        tables = soup.table.table
        tr = tables.find_all('tr')

        for i, item in enumerate(tr):
            if i == 0:
                continue
            td = item.find_all('td')
            head = 'http://aomp.judicial.gov.tw/abbs/wkw/'
            href = head + td[4].a['href']
            print(str((page-1)*15+i) + ", " + href)

            parser(href)
            # break

        page += 1


def main():
    key = get_key()

    courts = ["TPD", "PCD", "SLD", "TYD", "SCD", "MLD", "TCD", "NTD", "CHD", "ULD",
              "CYD", "TND", "KSD", "PTD", "TTD", "HLD", "ILD", "KLD", "PHD", "KMD", "LCD"]
    props = ["C52", "C51"]
    sales = ["1", "4", "5"]

    # for c in courts:
    #     for p in props:
    #         for s in sales:
    #             traverse(c, p, s)
    traverse(courts[16], props[1], sales[2], key)


def get_key():
    addr = "http://aomp.judicial.gov.tw/abbs/wkw/WHD2A02.jsp?proptype=C52&saletype=1&court=TPD"
    r = requests.get(addr)

    soup = BeautifulSoup(r.text, "html.parser")
    key = soup.input
    # print(key['name'])
    # print(key['value'])

    return key['name'] + "=" + key['value']

if __name__ == '__main__':
    main()
