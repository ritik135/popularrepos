from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from scrapper.views import init_driver


class PopularContribCommitListView(APIView):
    def post(self, request):

        org = 'org:'+str(request.data['org'])
        popular_repo_list = init_driver(org, request.data['n'], request.data['m'])
        if popular_repo_list is not None:
            return Response(popular_repo_list, status=status.HTTP_200_OK)
        else:
            return Response({"Message":"There is some issue during execution."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
