from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    def identity(self, options):
        out = []

        if len(options) == 0:
            raise(Exception('Error: no hay opciones'))

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            })

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def equality(self, options):
        out = []

        if len(options) == 0:
            raise(Exception('Error: no hay opciones'))

        hombres = 0
        mujeres = 0
        for opt in options:
            mujeres += opt['votesM']
            hombres += opt['votesH']
            
        if hombres == 0:

            for opt in options:
                votos = opt['votesM']

                out.append({
                    **opt,
                    'postproc': votos,
                })

        elif mujeres == 0:

            for opt in options:
                votos = opt['votesH']

                out.append({
                    **opt,
                    'postproc': votos,
                })

        else:

            for opt in options:
                if mujeres > hombres:
                    votos = opt['votesH'] + opt['votesM'] * (hombres / mujeres)
                else:
                    votos = opt['votesM'] + opt['votesH'] * (mujeres / hombres)

                out.append({
                    **opt,
                    'postproc': round(votos),
                })

        out.sort(key=lambda x: -x['postproc'])

        return Response(out)

    def borda(self, options):
        out = []

        if len(options) == 0:
            raise(Exception('Error: no hay opciones'))

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
        if t == 'EQUALITY':
            return self.equality(opts)

        return Response({})
