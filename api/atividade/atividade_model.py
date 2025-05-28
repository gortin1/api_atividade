from database import db
from datetime import datetime, timezone

class Atividade(db.Model):
    __tablename__ = 'atividades'

    id = db.Column(db.Integer, primary_key=True)
    professor_id = db.Column(db.Integer, nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    disciplina = db.Column(db.String(50), nullable=True)
    data_entrega = db.Column(db.Date, nullable=True)
    hora_fim = db.Column(db.Time, nullable=True)
    data_criacao = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __init__(
            self, 
            professor_id,  
            titulo,
            descricao,
            disciplina,
            data_entrega,
            hora_fim
            ):

            self.professor_id = professor_id
            self.titulo = titulo
            self.descricao = descricao
            self.disciplina = disciplina
            self.data_entrega = data_entrega
            self.hora_fim = hora_fim

    def to_dict(self):
            return {
                "id" : self.id,
                "professor_id" : self.professor_id,
                "titulo" : self.titulo,
                "descricao" : self.descricao,
                "disciplina" : self.disciplina,
                "data_entrega" : self.data_entrega.isoformat() if self.data_entrega else None,
                "hora_fim" : self.hora_fim.strftime("%H:%M") if self.hora_fim else None,
                "data_criacao" : self.data_criacao.strftime("%Y-%m-%d %H:%M:%S") if self.data_criacao else None                
            }   

class AtividadeNaoEncontrada(Exception):
    pass

def listar_atividades():
    atividades = Atividade.query.all()
    return [atividade.to_dict() for atividade in atividades]

def atividade_por_id(id):
    atividade = Atividade.query.get(id)

    if not atividade:
        raise AtividadeNaoEncontrada(f"Atividade não encontrada.")
    return atividade.to_dict()

def adicionar_atividade(novos_dados):
    try:
        professor_id = novos_dados['professor_id']
        titulo = novos_dados['titulo']
        descricao = novos_dados['descricao']
        disciplina = novos_dados.get('disciplina')
        data_entrega_str = novos_dados.get('data_entrega')
        hora_fim_str = novos_dados.get('hora_fim')
         
        data_entrega = datetime.strptime(data_entrega_str, "%Y-%m-%d").date() if data_entrega_str else None
        hora_fim = datetime.strptime(hora_fim_str, "%H:%M").time() if hora_fim_str else None



        nova_atividade = Atividade(
            professor_id = professor_id,
            titulo = titulo,
            descricao = descricao,
            disciplina = disciplina,
            data_entrega=data_entrega,
            hora_fim = hora_fim
        )

        db.session.add(nova_atividade)
        db.session.commit()
        return {'message': 'Atividade adicionada com sucesso.'}, 201

    except KeyError as e:
        return {'erro': 'Campo obrigatório ausente.', 'detalhes': str(e)}, 400
    except ValueError as e:
        return {'erro': 'Formato de data ou hora inválido.', 'detalhes': str(e)}, 400
    except Exception as e:
        return {'erro': 'Erro interno no servidor.', 'detalhes': str(e)}, 500


def atualizar_atividade(id, novos_dados):
    try:
        atividade = Atividade.query.get(id)
        if not atividade:
            raise AtividadeNaoEncontrada(f"Atividade não encontrada.")
        
        atividade.professor_id = novos_dados['professor_id']
        atividade.titulo = novos_dados['titulo']
        atividade.descricao = novos_dados['descricao']

        if 'disciplina' in novos_dados:
            atividade.disciplina = novos_dados['disciplina']

        if 'data_entrega' in novos_dados:
            data_entrega_str = novos_dados['data_entrega']
            atividade.data_entrega = datetime.strptime(data_entrega_str, "%Y-%m-%d").date() if data_entrega_str else None

        if 'hora_fim' in novos_dados:
            hora_fim_str = novos_dados['hora_fim']
            atividade.hora_fim = datetime.strptime(hora_fim_str, "%H:%M").time() if hora_fim_str else None
        
        db.session.commit()
        return {'message': 'Atividade atualizada com sucesso.'}, 200
    
    except KeyError as e:
        return {'erro': 'Campo obrigatório ausente.', 'detalhes': str(e)}, 400
    except ValueError as e:
        return {'erro': 'Formato de data ou hora inválido.', 'detalhes': str(e)}, 400
    except Exception as e:
        return {'erro': 'Erro interno no servidor.', 'detalhes': str(e)}, 500

def excluir_atividade(id):
    atividade = Atividade.query.get(id)
    if not atividade:
        raise AtividadeNaoEncontrada(f"Atividade não encontrada.")

    db.session.delete(atividade)
    db.session.commit()
    return {'message': 'Atividade excluída com sucesso.'}, 200