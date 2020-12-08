import json
import urllib

from bs4 import BeautifulSoup

import requests

from rankService.rank.rank import Rank


def buildRankList(keyword, company):
    # keywords = str(keywords).split(',')

    # ranks = []
    # rawDataList = getRawDataFromHtml(keyword)
    # if rawDataList:
    #     for rawData in rawDataList:
    #         if 'adId' not in rawData['item']:
    #             rankNo = rawData['item']['rank']
    #             imageurl = rawData['item']['imageUrl']
    #             title = rawData['item']['mallName']
    #             if not title:
    #                 title = rawData['item']['productTitle']
    #             rank = Rank(rankNo, imageurl, title)
    #             ranks.append(rank)
    # return filterRankList(ranks, company)
    return filterRankList(getRankListFromApi(keyword), company)


def getRawDataFromHtml(keyword):
    rawDataList = []
    for page in range(1, 11):
        naverResponse = requests.get(
            'https://search.shopping.naver.com/search/all?frm=NVSHATC&pagingIndex={}&pagingSize=100&productSet=total&query={}&sort=rel&timestamp=&viewType=list'.format(
                page, keyword))
        dom = BeautifulSoup(naverResponse.text, 'html.parser')
        if dom:
            jsonStr = dom.select_one('#__NEXT_DATA__').string
            if jsonStr:
                obj = json.loads(jsonStr)
                rawDataList.extend(obj['props']['pageProps']['initialState']['products']['list'])

    return rawDataList


def getRankListFromApi(keyword):
    # API 를 통해서 데이타를 가지고오도록
    client_id = "qFSZ7CaGt_phK2z_xBbj"
    client_secret = "t069sHymoW"
    ranks = []
    keyword = urllib.parse.quote(keyword)

    for idx in range(1, 1000, 100):
        url = "https://openapi.naver.com/v1/search/shop?query={}&display={}&start={}".format(keyword, 100, idx)
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)

        rescode = response.getcode()

        if rescode == 200:
            response_body = response.read()
            response_dict = json.loads(response_body.decode('utf-8'))
            items = response_dict['items']
            for item_index in range(0, len(items)):
                url = items[item_index]['link']
                imageurl = items[item_index]['image']
                productId = items[item_index]['productId']
                mallname = items[item_index]['mallName']
                title = items[item_index]['title']

                rank = Rank(0, url, imageurl, mallname, title, productId)
                ranks.append(rank)

        else:
            print("Error Code:" + rescode)

    return ranks


def filterRankList(ranks, company):
    # DB 저장을 위해 최상위만 검색한다.
    filteredRankList = []
    for idx in range(0, len(ranks)):  # ranks 가 없을 경우 에러발생될음 수 있음
        rank = ranks[idx]
        if rank.mallname.find(company) > -1:
            rank.rank = idx + 1
            filteredRankList.append(rank)
            break

    return filteredRankList
