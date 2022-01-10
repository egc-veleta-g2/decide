from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    def testIdentity(self):
        datos = {
            'type': 'IDENTITY',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        resultado = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', datos, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, resultado)

    def testIdentitySinOpciones(self):
        with self.assertRaises(Exception):
            datos = {
                'type': 'IDENTITY',
                'options': []
            }

            response = self.client.post('/postproc/', datos, format='json')
            self.assertEqual(response.status_code, 200)

    def testIdentityNoVotes(self):
        datos = {
            'type': 'IDENTITY',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 0 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 0 },
                { 'option': 'Option 4', 'number': 4, 'votes': 0 },
                { 'option': 'Option 5', 'number': 5, 'votes': 0 },
                { 'option': 'Option 6', 'number': 6, 'votes': 0 },
            ]
        }

        resultado = [
            { 'option': 'Option 1', 'number': 1, 'votes': 0, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
            { 'option': 'Option 3', 'number': 3, 'votes': 0, 'postproc': 0 },
            { 'option': 'Option 4', 'number': 4, 'votes': 0, 'postproc': 0 },
            { 'option': 'Option 5', 'number': 5, 'votes': 0, 'postproc': 0 },
            { 'option': 'Option 6', 'number': 6, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', datos, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, resultado)

    def testIdentitySinOption(self):
        with self.assertRaises(Exception):
            datos = {
                'type': 'IDENTITY'
            }

            response = self.client.post('/postproc/', datos, format='json')
            self.assertEqual(response.status_code, 200)


    def test_borda(self):
        datos = {
            'type': 'BORDA',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': [7, 2, 4, 2]},
                {'option': 'Option 2', 'number': 2, 'votes': [2, 8, 2, 3]},
                {'option': 'Option 3', 'number': 3, 'votes': [4, 4, 4, 3]},
                {'option': 'Option 4', 'number': 4, 'votes': [2, 1, 5, 7]},
            ]
        }

        resultado = [
            {'option': 'Option 1', 'number': 1, 'votes': [7, 2, 4, 2], 'postproc': 44},
            {'option': 'Option 2', 'number': 2, 'votes': [2, 8, 2, 3], 'postproc': 39},
            {'option': 'Option 3', 'number': 3, 'votes': [4, 4, 4, 3], 'postproc': 39},
            {'option': 'Option 4', 'number': 4, 'votes': [2, 1, 5, 7], 'postproc': 28},
        ]

        response = self.client.post('/postproc/', datos, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, resultado)

    def testBordaSinOpciones(self):
        with self.assertRaises(Exception):
            datos = {
                'type': 'BORDA',
                'options': []
            }

            response = self.client.post('/postproc/', datos, format='json')
            self.assertEqual(response.status_code, 200)

    def testBordaSinOption(self):
        with self.assertRaises(Exception):
            datos = {
                'type': 'BORDA'
            }

            response = self.client.post('/postproc/', datos, format='json')
            self.assertEqual(response.status_code, 200)

    def testBordaNoVotes(self):
        datos = {
            'type': 'BORDA',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': [0, 0, 0, 0]},
                {'option': 'Option 2', 'number': 2, 'votes': [0, 0, 0, 0]},
                {'option': 'Option 3', 'number': 3, 'votes': [0, 0, 0, 0]},
                {'option': 'Option 4', 'number': 4, 'votes': [0, 0, 0, 0]},
            ]
        }

        resultado = [
                {'option': 'Option 1', 'number': 1, 'votes': [0, 0, 0, 0], 'postproc': 0},
                {'option': 'Option 2', 'number': 2, 'votes': [0, 0, 0, 0], 'postproc': 0},
                {'option': 'Option 3', 'number': 3, 'votes': [0, 0, 0, 0], 'postproc': 0},
                {'option': 'Option 4', 'number': 4, 'votes': [0, 0, 0, 0], 'postproc': 0},
            ]

        response = self.client.post('/postproc/', datos, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, resultado)

    def testIgualdadMasMujeres(self):
        datos = {
            'type': 'EQUALITY',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votesH': 2, 'votesM': 3, 'votes': 0},
                {'option': 'Option 2', 'number': 2, 'votesH': 0, 'votesM': 4, 'votes': 0},
                {'option': 'Option 3', 'number': 3, 'votesH': 3, 'votesM': 1, 'votes': 0},
                {'option': 'Option 4', 'number': 4, 'votesH': 1, 'votesM': 0, 'votes': 0},
                {'option': 'Option 5', 'number': 5, 'votesH': 1, 'votesM': 3, 'votes': 0},
                {'option': 'Option 6', 'number': 6, 'votesH': 1, 'votesM': 1, 'votes': 0},
            ]
        }

        resultado = [
                {'option': 'Option 1', 'number': 1, 'votesH': 2, 'votesM': 3, 'votes': 0, 'postproc': 4},
                {'option': 'Option 3', 'number': 3, 'votesH': 3, 'votesM': 1, 'votes': 0, 'postproc': 4},
                {'option': 'Option 2', 'number': 2, 'votesH': 0, 'votesM': 4, 'votes': 0, 'postproc': 3},
                {'option': 'Option 5', 'number': 5, 'votesH': 1, 'votesM': 3, 'votes': 0, 'postproc': 3},
                {'option': 'Option 6', 'number': 6, 'votesH': 1, 'votesM': 1, 'votes': 0, 'postproc': 2},
                {'option': 'Option 4', 'number': 4, 'votesH': 1, 'votesM': 0, 'votes': 0, 'postproc': 1},
            ]


        response = self.client.post('/postproc/', datos, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, resultado)

    def testIgualdadSinMujeres(self):
        datos = {
            'type': 'EQUALITY',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votesH': 2, 'votesM': 0, 'votes': 0},
                {'option': 'Option 2', 'number': 2, 'votesH': 0, 'votesM': 0, 'votes': 0},
                {'option': 'Option 3', 'number': 3, 'votesH': 3, 'votesM': 0, 'votes': 0},
                {'option': 'Option 4', 'number': 4, 'votesH': 1, 'votesM': 0, 'votes': 0},
                {'option': 'Option 5', 'number': 5, 'votesH': 1, 'votesM': 0, 'votes': 0},
                {'option': 'Option 6', 'number': 6, 'votesH': 1, 'votesM': 0, 'votes': 0},
            ]
        }

        resultado = [
                {'option': 'Option 3', 'number': 3, 'votesH': 3, 'votesM': 0, 'votes': 0, 'postproc': 3},
                {'option': 'Option 1', 'number': 1, 'votesH': 2, 'votesM': 0, 'votes': 0, 'postproc': 2},
                {'option': 'Option 4', 'number': 4, 'votesH': 1, 'votesM': 0, 'votes': 0, 'postproc': 1},
                {'option': 'Option 5', 'number': 5, 'votesH': 1, 'votesM': 0, 'votes': 0, 'postproc': 1},
                {'option': 'Option 6', 'number': 6, 'votesH': 1, 'votesM': 0, 'votes': 0, 'postproc': 1},
                {'option': 'Option 2', 'number': 2, 'votesH': 0, 'votesM': 0, 'votes': 0, 'postproc': 0},
            ]


        response = self.client.post('/postproc/', datos, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, resultado)

    def testIgualdadMasHombres(self):
        datos = {
            'type': 'EQUALITY',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votesH': 3, 'votesM': 1, 'votes': 0},
                {'option': 'Option 2', 'number': 2, 'votesH': 1, 'votesM': 2, 'votes': 0},
                {'option': 'Option 3', 'number': 3, 'votesH': 2, 'votesM': 1, 'votes': 0},
                {'option': 'Option 4', 'number': 4, 'votesH': 0, 'votesM': 0, 'votes': 0},
                {'option': 'Option 5', 'number': 5, 'votesH': 1, 'votesM': 1, 'votes': 0},
                {'option': 'Option 6', 'number': 6, 'votesH': 3, 'votesM': 3, 'votes': 0},
            ]
        }

        resultado = [
                {'option': 'Option 6', 'number': 6, 'votesH': 3, 'votesM': 3, 'votes': 0, 'postproc': 5},
                {'option': 'Option 1', 'number': 1, 'votesH': 3, 'votesM': 1, 'votes': 0, 'postproc': 3},
                {'option': 'Option 2', 'number': 2, 'votesH': 1, 'votesM': 2, 'votes': 0, 'postproc': 3},
                {'option': 'Option 3', 'number': 3, 'votesH': 2, 'votesM': 1, 'votes': 0, 'postproc': 3},
                {'option': 'Option 5', 'number': 5, 'votesH': 1, 'votesM': 1, 'votes': 0, 'postproc': 2},
                {'option': 'Option 4', 'number': 4, 'votesH': 0, 'votesM': 0, 'votes': 0, 'postproc': 0},
            ]

        response = self.client.post('/postproc/', datos, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, resultado)

    def testIgualdadSinHombres(self):
        datos = {
            'type': 'EQUALITY',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votesH': 0, 'votesM': 1, 'votes': 0},
                {'option': 'Option 2', 'number': 2, 'votesH': 0, 'votesM': 2, 'votes': 0},
                {'option': 'Option 3', 'number': 3, 'votesH': 0, 'votesM': 1, 'votes': 0},
                {'option': 'Option 4', 'number': 4, 'votesH': 0, 'votesM': 0, 'votes': 0},
                {'option': 'Option 5', 'number': 5, 'votesH': 0, 'votesM': 1, 'votes': 0},
                {'option': 'Option 6', 'number': 6, 'votesH': 0, 'votesM': 3, 'votes': 0},
            ]
        }

        resultado = [
                {'option': 'Option 6', 'number': 6, 'votesH': 0, 'votesM': 3, 'votes': 0, 'postproc': 3},
                {'option': 'Option 2', 'number': 2, 'votesH': 0, 'votesM': 2, 'votes': 0, 'postproc': 2},
                {'option': 'Option 1', 'number': 1, 'votesH': 0, 'votesM': 1, 'votes': 0, 'postproc': 1},
                {'option': 'Option 3', 'number': 3, 'votesH': 0, 'votesM': 1, 'votes': 0, 'postproc': 1},
                {'option': 'Option 5', 'number': 5, 'votesH': 0, 'votesM': 1, 'votes': 0, 'postproc': 1},
                {'option': 'Option 4', 'number': 4, 'votesH': 0, 'votesM': 0, 'votes': 0, 'postproc': 0},
            ]

        response = self.client.post('/postproc/', datos, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, resultado)

    def testIgualdadNoVotes(self):
        datos = {
            'type': 'EQUALITY',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votesH': 0, 'votesM': 0, 'votes': 0},
                {'option': 'Option 2', 'number': 2, 'votesH': 0, 'votesM': 0, 'votes': 0},
                {'option': 'Option 3', 'number': 3, 'votesH': 0, 'votesM': 0, 'votes': 0},
                {'option': 'Option 4', 'number': 4, 'votesH': 0, 'votesM': 0, 'votes': 0},
                {'option': 'Option 5', 'number': 5, 'votesH': 0, 'votesM': 0, 'votes': 0},
                {'option': 'Option 6', 'number': 6, 'votesH': 0, 'votesM': 0, 'votes': 0},
            ]
        }

        resultado = [
                {'option': 'Option 1', 'number': 1, 'votesH': 0, 'votesM': 0, 'votes': 0, 'postproc': 0},
                {'option': 'Option 2', 'number': 2, 'votesH': 0, 'votesM': 0, 'votes': 0, 'postproc': 0},
                {'option': 'Option 3', 'number': 3, 'votesH': 0, 'votesM': 0, 'votes': 0, 'postproc': 0},
                {'option': 'Option 4', 'number': 4, 'votesH': 0, 'votesM': 0, 'votes': 0, 'postproc': 0},
                {'option': 'Option 5', 'number': 5, 'votesH': 0, 'votesM': 0, 'votes': 0, 'postproc': 0},
                {'option': 'Option 6', 'number': 6, 'votesH': 0, 'votesM': 0, 'votes': 0, 'postproc': 0},
            ]


        response = self.client.post('/postproc/', datos, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, resultado)

    def testIgualdadSinOption(self):
        with self.assertRaises(Exception):
            datos = {
                'type': 'EQUALITY'
            }
            response = self.client.post('/postproc/', datos, format='json')
            self.assertEqual(response.status_code, 200)

    def testIgualdadSinOpciones(self):
        with self.assertRaises(Exception):
            datos = {
                'type': 'EQUALITY',
                'options': []
            }

            response = self.client.post('/postproc/', datos, format='json')
            self.assertEqual(response.status_code, 200)

    def testSinType(self):
        datos = {
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        resultado = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', datos, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, resultado)

    def testIgualdadSinIndicarType(self):
    #   No ordena por genero, aunque tenga datos de genero
        datos = {
            'options': [
                {'option': 'Option 1', 'number': 1, 'votesH': 5, 'votesM': 1,  'votes': 1},
                {'option': 'Option 2', 'number': 2, 'votesH': 2, 'votesM': 2,  'votes': 2},
                {'option': 'Option 3', 'number': 3, 'votesH': 3, 'votesM': 1,  'votes': 1},
                {'option': 'Option 4', 'number': 4, 'votesH': 0, 'votesM': 0,  'votes': 0},
                {'option': 'Option 5', 'number': 5, 'votesH': 1, 'votesM': 1,  'votes': 1},
                {'option': 'Option 6', 'number': 6, 'votesH': 0, 'votesM': 3,  'votes': 3},
            ]
        }

        resultado = [
                {'option': 'Option 6', 'number': 6, 'votesH': 0, 'votesM': 3,  'votes': 3, 'postproc': 3},
                {'option': 'Option 2', 'number': 2, 'votesH': 2, 'votesM': 2,  'votes': 2, 'postproc': 2},
                {'option': 'Option 1', 'number': 1, 'votesH': 5, 'votesM': 1,  'votes': 1, 'postproc': 1},
                {'option': 'Option 3', 'number': 3, 'votesH': 3, 'votesM': 1,  'votes': 1, 'postproc': 1},
                {'option': 'Option 5', 'number': 5, 'votesH': 1, 'votesM': 1,  'votes': 1, 'postproc': 1},
                {'option': 'Option 4', 'number': 4, 'votesH': 0, 'votesM': 0,  'votes': 0, 'postproc': 0},
            ]

        response = self.client.post('/postproc/', datos, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, resultado)

    def testDatosVacio(self):
        with self.assertRaises(Exception):
            datos = {}
            response = self.client.post('/postproc/', datos, format='json')
            self.assertEqual(response.status_code, 200)

    def testIgualdadMismosHqueM(self):
        datos = {
            'type': 'EQUALITY',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votesH': 3, 'votesM': 3, 'votes': 0},
                {'option': 'Option 2', 'number': 2, 'votesH': 4, 'votesM': 4, 'votes': 0},
                {'option': 'Option 3', 'number': 3, 'votesH': 1, 'votesM': 1, 'votes': 0},
                {'option': 'Option 4', 'number': 4, 'votesH': 0, 'votesM': 0, 'votes': 0},
                {'option': 'Option 5', 'number': 5, 'votesH': 3, 'votesM': 3, 'votes': 0},
                {'option': 'Option 6', 'number': 6, 'votesH': 1, 'votesM': 1, 'votes': 0},
            ]
        }
            #   postproc = votesH + votesM
        resultado = [
                {'option': 'Option 2', 'number': 2, 'votesH': 4, 'votesM': 4, 'votes': 0, 'postproc': 8},
                {'option': 'Option 1', 'number': 1, 'votesH': 3, 'votesM': 3, 'votes': 0, 'postproc': 6},
                {'option': 'Option 5', 'number': 5, 'votesH': 3, 'votesM': 3, 'votes': 0, 'postproc': 6},
                {'option': 'Option 3', 'number': 3, 'votesH': 1, 'votesM': 1, 'votes': 0, 'postproc': 2},
                {'option': 'Option 6', 'number': 6, 'votesH': 1, 'votesM': 1, 'votes': 0, 'postproc': 2},
                {'option': 'Option 4', 'number': 4, 'votesH': 0, 'votesM': 0, 'votes': 0, 'postproc': 0},
            ]

        response = self.client.post('/postproc/', datos, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, resultado)