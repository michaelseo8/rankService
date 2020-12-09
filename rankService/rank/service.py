import json
import urllib
import sqlite3

from bs4 import BeautifulSoup

import requests

from rankService.rank.rank import Rank


def updateRankList(keyword, company, ranks):
    # 1. 키워드 + 회사명으로 저장된 정보가 있는지 확인 (SELECT). 없을 경우 keyword 테이블에 (INSERT)
    # 2. 해당 키워드 조합으로 최근 검색된 순위 정보가 있느지 확인 (SELECT), 있을 경우 최근 순위(latestRank) 에 저장.
    # 3. 키워드 + 회사명으로 네이버로 부터 받아온 최신 순위 정보를 rank_history 테이블에 저장 (INSERT)

    # 1.
    selectConn = sqlite3.connect('./db.sqlite3', timeout=10)  # oracle, mysql, etc....
    query = "SELECT keywordId FROM keyword WHERE keyword = ? AND company = ? LIMIT 1"
    selectCur = selectConn.cursor()
    selectCur.execute(query, (keyword, company))  # SELECT 쿼리를 실행!
    keywordRow = selectCur.fetchone()
    selectConn.commit()
    selectCur.close()
    selectConn.close()

    keywordId = None

    # 검색어 테이블에 없을 경우 입력
    if not keywordRow:  # 해당 keyword + company 로 처음 검색했을 경우
        insertConn = sqlite3.connect('./db.sqlite3', timeout=10)
        insertCur = insertConn.cursor()
        # keyword + company INSERT
        query = "INSERT INTO keyword (keyword, company, createdAt, updatedAt) values (?, ?, datetime('now'), datetime('now'))"
        insertCur.execute(query, (keyword, company))  # INSERT 쿼리를 실행!
        keywordId = insertCur.lastrowid  # 방금 입력된 keywordId 반환
        insertConn.commit()
        insertCur.close()
        insertConn.close()
    # 검색어 테이블에 있을 경우 해당 데이타 사용
    else:  # 해당 keyword + company 로 검색한 내역이 있을 경우
        keywordId = keywordRow[0]

    # 2.
    # latestRank 구하기
    selectConn = sqlite3.connect('./db.sqlite3', timeout=10)
    query = "SELECT rank, updatedAt FROM rank_history WHERE keywordId = ? ORDER BY rankHistoryId DESC LIMIT 1"  # 기존에 조회했던 순위 기록중 가장 최신의 것을 불러온다.
    selectCur = selectConn.cursor()
    selectCur.execute(query, (keywordId,))  # 순위검색 SELECT 쿼리 실행!
    rankHistoryRow = selectCur.fetchone()  # 가장 최근 순위 정보. (첫 검색일 경우 없다!)
    selectConn.commit()
    selectCur.close()
    selectConn.close()

    latestRank = None
    latestSearchDate = None

    if rankHistoryRow:
        latestRank = rankHistoryRow[0]
        latestSearchDate = rankHistoryRow[1]
    # 3.
    # rank_history insert
    updateConn = sqlite3.connect('./db.sqlite3', timeout=10)
    updateCur = updateConn.cursor()
    for rank in ranks:
        query = "INSERT INTO rank_history (keywordId, rank, createdAt, updatedAt) values (?, ?, datetime('now'), datetime('now'))"
        updateCur.execute(query, (keywordId, rank.rank))
        updateConn.commit()
        rank.latestRank = latestRank
        rank.latestSearchDate = latestSearchDate

    updateCur.close()
    updateConn.close()


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
