# rank/views.py
import json

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
from rankService.rank.service import buildRankList, updateRankList

# class 선언시 클래스명 뒤에 () 안에 오는 또 다른 클래스는 ()안에 클래스를 '상속' 받아서 사용한다는 뜻
class RankListView(TemplateView):
    # TemplateView 에 이미 선언되어 있음
    template_name = "rank/list.html"

    # TemplateView 에 들어온 get 요청 처리
    def get(self, request, *args, **kwargs):
        # 템플릿에 전달할 데이타
        ctx = {}
        # TemplateView 에서 제공하는 함수로, 위에 선언한 템플릿에 ctx 라 데이타를 전달하여 렌더링(HTML을 그림) 한다.
        return self.render_to_response(ctx)

    # TemplateView 에 들어온 post 요청 처리
    # def post(self, request, *args, **kwargs):
    #     keyword = request.POST.get('keyword')
    #     company = request.POST.get('company')
    #     # 네이버API 를 통해 해당 keyword로 검색된 결과중 company 와 일치하는 가장 높은 순위 1개 결과 반환.
    #     ranks = buildRankList(keyword, company)
    #     if ranks:
    #         # 최근 순위 화면용 변수에 저장, 검색 히스토리 및 검색어 DB 에 저장
    #         updateRankList(keyword, company, ranks)
    #     ctx = {"keyword": keyword, "company": company, "ranks": ranks}
    #     return self.render_to_response(ctx)  # TemplateView 에서 제공하는 함수로, 위에 선언한 템플릿에 ctx 라 데이타를 전달하여 렌더링(HTML을 그림) 한다.


def rankDataProvider(request):
    keyword = request.GET.get('keyword')
    company = request.GET.get('company')
    # # 네이버API 를 통해 해당 keyword로 검색된 결과중 company 와 일치하는 가장 높은 순위 1개 결과 반환.
    ranks = {}
    if keyword and company:
        ranks = buildRankList(keyword, company)
        if ranks:
            # 최근 순위 화면용 변수에 저장, 검색 히스토리 및 검색어 DB 에 저장
            updateRankList(keyword, company, ranks)

    rank = json.dumps(ranks[0].__dict__)
    return HttpResponse(rank, content_type="application/json")