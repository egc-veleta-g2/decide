from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            })

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def borda(self, options):
        out = []

        if len(options) == 0:
            raise(Exception('Bad request: There no options'))

        for opt in options:
            numVotes = 0
            numOptions = len(options)
            for i in range(0, numOptions):
                numVotes += opt['votes'][i] * (numOptions - i)
            out.append({
                **opt,
                'postproc': numVotes,
            })

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """


        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)
        if t == 'BORDA':
            return self.borda(opts)

        #out.append({'type': t, 'options': result})

        return Response({})
