from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from scrapper.views import init_driver


class PopularContribCommitListView(APIView):
    def post(self, request):

        print('org:'+str(request.data['org']))
        print(request.data['n'])
        print(request.data['m'])

        org = 'org:'+str(request.data['org'])
        popular_repo_list = init_driver(org, request.data['n'], request.data['m'])

        return Response(popular_repo_list, status=status.HTTP_200_OK)
