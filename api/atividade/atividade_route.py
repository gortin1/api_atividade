from flask import Blueprint, request, jsonify
import requests
from api.atividade.atividade_model import AtividadeNaoEncontrada, atividade_por_id, listar_atividades, adicionar_atividade, atualizar_atividade, excluir_atividade

atividades_blueprint = Blueprint("atividades", __name__)

def validar_professor(professor_id):
    response = requests.get(f"http://localhost:5000/api/professores/{professor_id}")
    return response.status_code == 200


@atividades_blueprint.route('/atividades', methods = ['POST'])
def create_atividade():
    try:
        dados = request.json
        professor_id = dados.get("professor_id")

        if not validar_professor(professor_id):
            return jsonify({'erro': 'Professor não encontrado'}), 404

        response, status_code = adicionar_atividade(dados)
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'erro': 'Erro interno no servidor.', 'detalhes': str(e)}), 500

@atividades_blueprint.route('/atividades', methods = ['GET'])
def get_atividades():
    return jsonify(listar_atividades()), 200

@atividades_blueprint.route('/atividades/<int:id>', methods = ['GET'])
def get_atividade(id):
    try:
        atividade = atividade_por_id(id)
        return jsonify(atividade), 200
    except AtividadeNaoEncontrada:
        return jsonify({'erro': 'Atividade não encontrada.'}), 404

@atividades_blueprint.route('/atividades/<int:id>', methods = ['PUT'])
def update_atividade(id):
    dados = request.json
    professor_id = dados.get("professor_id")

    if not validar_professor(professor_id):
        return jsonify({'erro': 'Professor não encontrado'}), 404
    
    try: 
        atualizar_atividade(id, dados)
        atividade_atualizada = atividade_por_id(id)
        return jsonify({
            'message': 'Atividade atualizada com sucesso.',
            'atividade': atividade_atualizada
        }), 200
    except AtividadeNaoEncontrada:
        return jsonify({'erro': 'Atividade não encontrada.'}), 404

@atividades_blueprint.route('/atividades/<int:id>', methods=['DELETE'])
def delete_atividade(id):
    try:
        excluir_atividade(id)
        return jsonify({'message': 'Atividade excluída com sucesso.'}), 200
    except AtividadeNaoEncontrada:
        return jsonify({'erro': 'Atividade não encontrada.'}), 404