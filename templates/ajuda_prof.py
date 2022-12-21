from checar_sessao import *
from rotas_direcao import Direcao
from rotas_responsavel import Responsavel
from rotas_aluno import Aluno
from rotas_professor import Professor


class AjudaProf:

    def __init__(self, app):
        @app.route('/')
        def primeira_tela():
            session.pop('user_p', None)
            session.pop('user_a', None)
            session.pop('user_r', None)
            session.pop('user_d', None)
            return render_template('primeira_tela.html')

        # rotas do prof começam aqui
        Professor(app)

        # rotas do aluno começam aqui
        Aluno(app)

        # rotas do responsavel começam aqui
        Responsavel(app)

        # rotas da diretoria começam aqui
        Direcao(app)



