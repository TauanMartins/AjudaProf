from checar_sessao import *


class Responsavel:
    def __init__(self, app):
        # rotas do responsavel começam aqui
        # abaixo é feito a primeira solicitação do login que caíra no GET
        # e que renderizará o template do login onde o usuario colocará os dados
        # após isso ele fará um request = post em /login_p novamente e
        # entrará na primeira condição que o redireciona para /menu_principal_resp
        @app.route('/login_r', methods=['POST', 'GET'])
        def login_responsaveis():
            if request.method == 'POST':
                # pega oq o resp digitou no usuario
                usuario_r = request.form['usuario_r']

                # abre o banco de dados
                mysql = bd.SQL()

                # puxa do banco de dados info(usuario) do usuário q
                # logou, isso puxará a validação para permitir a entrada
                comando = "SELECT cpf_responsavel AS cpf, nme_responsavel as nome " \
                          "FROM tb_responsavel WHERE cpf_responsavel=%s;"
                cs = mysql.consultar(comando, [usuario_r])

                # se existir o cpf no banco de dados que o usuario digitou,
                # esta ficará armazenada em dados, se n, vai entrar
                # na primeira condiçao onde retornará dados invalidos
                dados = cs.fetchone()
                if dados is None:
                    return redirect('/login_r')

                # abaixo haverá a validação: comparando oq o usuario digitou e
                # oq está no banco de dados. Se existir, será redirecionado para
                # a o menu principal do resp, caso não exista redireciona p login
                if dados[0] == usuario_r:
                    session.permanent = True
                    session['user_r'] = usuario_r
                    return redirect('/menu_principal_resp')
                elif dados[0] != usuario_r:
                    return redirect('/login_r')

            # abaixo um metodo get
            else:
                # if abaixo valida se o usuário ja estava logada na maquina
                # permitindo uma entrada mais rápida.
                if "user_r" in session:
                    return redirect('/menu_principal_resp')
                return render_template('login_r.html')

        @app.route('/menu_principal_resp', methods=['POST', 'GET'])
        @checar_sessao_responsavel
        def menu_principal_resp():
            return "a"