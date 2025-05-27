import unittest
import requests

class TestAtividade(unittest.TestCase):

    def test_001_cria_atividades(self):
        response1 = requests.post('http://localhost:5003/atividades', json={
            "professor_id": 2,
            "titulo": "Api Gestão Escolar",
            "descricao": "Desenvolver Api com Python e Flask",
            "disciplina": "Api e Microsserviços",
            "data_entrega": "2025-05-25",
            "hora_fim": "10:00"
        })

        response2 = requests.post('http://localhost:5003/atividades', json={
            "professor_id": 3,
            "titulo": "Sistema de Reservas",
            "descricao": "Criar sistema com autenticação JWT",
            "disciplina": "Segurança e API",
            "data_entrega": "2025-06-01",
            "hora_fim": "11:00"
        })

        self.assertEqual(response1.status_code, 201)
        self.assertIn("Atividade adicionada com sucesso.", response1.text)
        self.assertEqual(response2.status_code, 201)
        self.assertIn("Atividade adicionada com sucesso.", response2.text)

    def test_002_lista_atividades(self):
        response = requests.get('http://localhost:5003/atividades')
        if response.status_code == 404:
            self.fail("Erro 404 - Não há atividades no servidor")
        try:
            lista = response.json()
        except:
            self.fail("Não retornou JSON na listagem de atividades")
        self.assertIsInstance(lista, list)

    def test_003_atividade_por_id(self):
        atividade_id = requests.get('http://localhost:5003/atividades/1')
        dict_retornado = atividade_id.json()
        self.assertEqual(type(dict_retornado), dict)
        self.assertIn('titulo', dict_retornado)
        self.assertEqual(dict_retornado['titulo'], 'Api Gestão Escolar')

    def test_004_edita_atividade(self):
        requests.post('http://localhost:5003/atividades', json={
            "professor_id": 4,
            "titulo": "Projeto Android",
            "descricao": "Criar app de clima com consumo de API",
            "disciplina": "Mobile Development",
            "data_entrega": "2025-06-05",
            "hora_fim": "09:30"
        })

        response_antes = requests.get('http://localhost:5003/atividades/3')
        self.assertEqual(response_antes.json()['titulo'], "Projeto Android")

        requests.put('http://localhost:5003/atividades/3', json={
            "professor_id": 4,
            "titulo": "App Clima Moderno",
            "descricao": "Atualizar layout",
            "disciplina": "UX Design",
            "data_entrega": "2025-06-10",
            "hora_fim": "10:00"
        })

        response_depois = requests.get('http://localhost:5003/atividades/3')
        atividade_json = response_depois.json()
        self.assertEqual(atividade_json['titulo'], "App Clima Moderno")
        self.assertEqual(atividade_json['disciplina'], "UX Design")

    def test_005_deleta_atividade(self):
        requests.post('http://localhost:5003/atividades', json={
            "professor_id": 4,
            "titulo": "Dashboard com Power BI",
            "descricao": "Criar relatório interativo de vendas",
            "disciplina": "Business Intelligence",
            "data_entrega": "2025-06-08",
            "hora_fim": "16:00"
        })

        requests.delete('http://localhost:5003/atividades/4')

        response_check = requests.get('http://localhost:5003/atividades/4')
        self.assertEqual(response_check.status_code, 404)


def runTests():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestAtividade)
    unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)

if __name__ == '__main__':
    runTests()
