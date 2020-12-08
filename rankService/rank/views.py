# rank/views.py

from django.views.generic import TemplateView
from rankService.rank.service import buildRankList, updateRankList


# class 선언시 클래스명 뒤에 () 안에 오는 또 다른 클래스는 ()안에 클래스를 '상속' 받아서 사용한다는 뜻
class RankListView(TemplateView):
    # TemplateView 에 이미 선언되어 있음
    template_name = "rank/list.html"

    # TemplateView 에 들어온 get 요청 처리
    def get(self, request, *args, **kwargs):
        ctx = {}  # 템플릿에 전달할 데이타
        return self.render_to_response(ctx)  # TemplateView 에서 제공하는 함수로, 위에 선언한 템플릿에 ctx 라 데이타를 전달하여 렌더링(HTML을 그림) 한다.

    # TemplateView 에 들어온 post 요청 처리
    def post(self, request, *args, **kwargs):
        keyword = request.POST.get('keyword')
        company = request.POST.get('company')
        ranks = buildRankList(keyword, company)
        ctx = {"keyword": keyword, "company": company, "ranks": ranks}

        # if ranks:
        updateRankList(keyword, company, ranks)

        return self.render_to_response(ctx)  # TemplateView 에서 제공하는 함수로, 위에 선언한 템플릿에 ctx 라 데이타를 전달하여 렌더링(HTML을 그림) 한다.