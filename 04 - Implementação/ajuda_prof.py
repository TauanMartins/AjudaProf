from flask import Flask, render_template, request, redirect, session
import bd
from checker_prof import check_logged_in_p
from checker_aluno import check_logged_in_a
from datetime import timedelta


class AjudaProf:
    def __init__(self):

        def printar(msg):
            print(msg)

        @app.route('/')
        def primeira_tela():
            return render_template('primeira_tela.html')

        @app.route('/logout_p', methods=['POST', 'GET'])
        def logout_p():
            session.pop('user_p', None)
            return render_template('logout.html')

        @app.route('/logout_a', methods=['POST', 'GET'])
        def logout_a():
            session.pop('user_a', None)
            return render_template('logout.html')

        # rotas do prof começam aqui
        # abaixo é feito a primeira solicitação do login que caíra no ultimo else
        # após isso renderiza o template do login onde o usuario colocará os dados
        # após isso ele dá um request = post em /login_p novamente
        # entra na primeira condição que o redireciona para /menu_principal_prof
        @app.route('/login_p', methods=['POST', 'GET'])
        def login_professor():
            if request.method == "POST":
                # pega oq o prof digitou no usuario e senha
                usuario_p = request.form['usuario_p']
                senha_p = request.form['senha_p']
                session.permanent = True
                session['user_p'] = usuario_p
                # abre o banco de dados
                mysql = bd.SQL()

                # puxa do banco de dados daquele usuário(idt) o usuario e senha para validar
                comando = f"SELECT matricula_professor AS usuario," \
                          f" senha_professor AS senha, nme_professor as nome FROM tb_professor " \
                          f"WHERE matricula_professor=%s AND senha_professor=%s;"
                cs = mysql.consultar(comando, [int(usuario_p), senha_p])
                # se existir a matricula no banco de dados que o usuario digitou,
                # esta ficará armazenada em dados, se n, vai entrar
                # na primeira condiçao onde retornará dados invalidos
                dados = cs.fetchone()

                if dados is None:
                    return redirect('/login_p')

                # se existirem dados validos que batem com oq há no bd entrará no else abaixo
                else:
                    return redirect('/menu_principal_prof')
            else:
                if "user_p" in session:
                    return redirect('/menu_principal_prof')
                return render_template('login_p.html')

        @app.route('/menu_principal_prof', methods=['POST', 'GET'])
        @check_logged_in_p
        def menu_principal_prof():
            mysql = bd.SQL()
            comando = f"SELECT nme_professor as nome FROM tb_professor WHERE matricula_professor=%s;"
            cs = mysql.consultar(comando, [int(session['user_p'])])
            dados = cs.fetchone()
            msg = f"entrou, bem vindo {dados[0]}"
            return render_template('menu_prof.html', msg=msg)

        @app.route('/alterar_notas', methods=["POST", "GET"])
        @check_logged_in_p
        def alterar_notas():
            return render_template('alterar_notas.html')

        @app.route('/alterar_presenca', methods=['POST'])
        @check_logged_in_p
        def alterar_presenca():
            # renderiza o html de alterar atividades e presença
            return 'entrou'

        @app.route('/editar_perfil_p')
        @check_logged_in_p
        def editar_perfil_p():
            # renderiza o html de editar perfil do prof
            pass

        # rotas do prof acabam aqui
        # rotas do aluno começam aqui
        # abaixo é feito a primeira solicitação do login que caíra no ultimo else
        # após isso renderiza o template do login onde o usuario colocará os dados
        # após isso ele dá um request = post em /login_p novamente
        # entra na primeira condição que o redireciona para /menu_principal_prof
        @app.route('/login_a', methods=["POST", "GET"])
        def login_aluno():
            if request.method == "POST":
                # pega oq o aluno digitou no usuario e senha
                usuario_a = int(request.form['usuario_a'])
                senha_a = request.form['senha_a']
                session.permanent = True
                session['user_a'] = usuario_a
                # abre o banco de dados
                mysql = bd.SQL()

                # puxa do banco de dados daquele usuário(idt) o usuario e senha para validar
                comando = f"SELECT matricula_aluno AS usuario, senha_aluno AS senha, nme_aluno as nome FROM tb_aluno " \
                          f"WHERE matricula_aluno=%s AND senha_aluno=%s;"
                cs = mysql.consultar(comando, [usuario_a, senha_a])

                # se existir a matricula no banco de dados que o usuario digitou,
                # esta ficará armazenada em dados, se n, vai entrar
                # na primeira condiçao onde retornará dados invalidos
                dados = cs.fetchone()
                if dados is None:
                    return redirect('/login_a')

                # se existirem dados validos que batem com oq há no bd entrará no else abaixo
                else:
                    return redirect('/menu_principal_aluno')
            else:
                if "user_a" in session:
                    return redirect('/menu_principal_aluno')
                return render_template('login_a.html')

        @app.route('/menu_principal_aluno', methods=['POST', 'GET'])
        @check_logged_in_a
        def menu_principal_aluno():
            msg = "Entrou"
            return render_template('teste_de_login.html')

        @app.route('/ver_notas')
        @check_logged_in_a
        def notas():
            # renderiza o html notas
            pass

        @app.route('/ver_presenca_e_atividades')
        @check_logged_in_a
        def presenca_e_atividades():
            # renderiza o html atividades e presença
            pass

        @app.route('/editar_perfil_a')
        @check_logged_in_a
        def editar_perfil_a():
            # renderiza o html de editar perfil
            pass

        @app.route('/esqueci_senha')
        def esqueci_senha():
            # renderiza o html de esqueci a senha POS(login)
            pass

        @app.route('/primeiro_acesso')
        def primeiro_acesso():
            # renderiza o html de primeiro acesso POS(login)
            pass

        # rotas do aluno acabam aqui
        # rotas do responsavel começam aqui

        @app.route('/login_r')
        def login_responsaveis():
            return render_template('login_r.html')

        @app.route('/menu_principal_resp', methods=['POST'])
        def menu_principal_resp():
            # pega oq o prof digitou no usuario e senha
            usuario_r = int(request.form['usuario_r'])

            # abre o banco de dados
            mysql = bd.SQL()

            # puxa do banco de dados daquele usuário(idt) o usuario e senha para validar
            comando = f"SELECT cpf_responsavel AS cpf, nme_responsavel as nome " \
                      f"FROM tb_responsavel WHERE cpf_responsavel=%s;"
            cs = mysql.consultar(comando, [usuario_r])

            # se existir a matricula no banco de dados que o usuario digitou,
            # esta ficará armazenada em dados, se n, vai entrar
            # na primeira condiçao onde retornará dados invalidos
            dados = cs.fetchone()

            if dados is None:
                return redirect('/login_r')
            usuario = dados[0]

            # abaixo haverá a validação: comparando oq o usuario digitou e oq está no banco de dados
            if usuario == usuario_r:
                msg = f"entrou, bem vindo {dados[1]}"
                return render_template('teste_de_login.html', msg=msg)
            elif usuario != usuario_r:
                return redirect('/login_r')

        # rotas do responsavel acabam aqui


app = Flask(__name__)
app.secret_key = "SenhaSecreta"
app.permanent_session_lifetime = timedelta(minutes=60)
AjudaProf()
if __name__ == '__main__':
    app.run(debug=True)
