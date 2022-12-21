from checar_sessao import *


class Aluno:
    def __init__(self, app):

        def verify_password(senha_crip, senha):
            return check_password_hash(senha_crip, senha)

        # abaixo é feito a primeira solicitação do login que caíra no GET
        # após isso renderiza o template do login onde o usuario colocará os dados
        # após isso ele fará um request = post em /login_p novamente e
        # entrará na primeira condição que o redireciona para /menu_principal_prof
        @app.route('/login_a', methods=["POST", "GET"])
        def login_aluno():

            if request.method == "POST":
                # pega os dados que o aluno digitou no usuario e senha
                usuario_a = request.form['usuario_a']
                senha_a = request.form['senha_a']

                # abre o banco de dados
                mysql = bd.SQL()

                # puxa do banco de dados info(usuario e senha) do usuário q
                # logou, isso puxará a senha para a validação
                comando = "SELECT matricula_aluno AS usuario, senha_aluno AS senha, nme_aluno " \
                          "as nome FROM tb_aluno WHERE matricula_aluno=%s;"
                cs = mysql.consultar(comando, [usuario_a])

                # se existir a matricula no banco de dados que o usuario digitou,
                # esta ficará armazenada em dados, se n existir, vai entrar condiçao
                # onde retornará dados invalidos e requisitara outro login
                dados = cs.fetchone()
                if dados is None:
                    return redirect('/login_a')
                if not (verify_password(dados[1], senha_a)):
                    return redirect('/login_a')

                # se existirem dados validos o programa retorna o elif
                # abaixo, permitindo o usuario entrar no menu principal
                elif verify_password(dados[1], senha_a):
                    session.permanent = True
                    session['user_a'] = usuario_a
                    return redirect('/menu_principal_aluno')

            # abaixo um comando get
            else:
                # if abaixo valida se o usuário ja estava logada na maquina
                # permitindo uma entrada mais rápida.
                if "user_a" in session:
                    return redirect('/menu_principal_aluno')
                return render_template('login_a.html')

        @app.route('/menu_principal_aluno', methods=['POST', 'GET'])
        @checar_sessao_aluno
        def menu_principal_aluno():
            return render_template('menu_principal_aluno.html')

        @app.route('/ver_notas', methods=['POST', 'GET'])
        @checar_sessao_aluno
        def notas():
            return render_template("ver_notas.html")

        @app.route('/ver_presenca_e_atividades', methods=['POST', 'GET'])
        @checar_sessao_aluno
        def presenca_e_atividades():
            # renderiza o html atividades e presença
            return render_template("visualizar_presenca.html")

        @app.route('/editar_perfil_a', methods=['POST', 'GET'])
        @checar_sessao_aluno
        def editar_perfil_a():
            # comando get para renderizar o html de editar perfil do aluno
            if request.method == "GET":
                # abre o banco de dados para mostrar todos os dados p alterar
                mysql = bd.SQL()
                comando = "SELECT * FROM tb_aluno JOIN tb_turma ON " \
                          "idt_serie_turma=cod_turma WHERE matricula_aluno=%s;"
                cs = mysql.consultar(comando, [session['user_a']])
                dados = cs.fetchone()

                return render_template('editar_perfil_aluno.html',
                                       nome=dados[1], nasc=dados[4], mao=dados[5],
                                       matricula=dados[3], sangue=dados[6], serie=dados[9])

            elif request.method == "POST":
                # metodo post para alteração dos dados, abaixo é puxado todos
                # os dados alterados do professor e faz o update no banco
                mao = request.form["mao"]
                sangue = request.form["sangue"]

                # abre o banco para fazer o update
                mysql = bd.SQL()
                comando = "UPDATE tb_aluno SET mao_aluno=%s, sangue_aluno=%s " \
                          "WHERE matricula_aluno=%s;"
                mysql.executar(comando, [mao, sangue, session['user_a']])
                mysql.cnx.commit()
                return 'ok'

        @app.route('/esqueci_senha', methods=['POST', 'GET'])
        def esqueci_senha():
            # renderiza o html de esqueci a senha POS(login)
            return render_template('esqueci_senha.html')

        @app.route('/primeiro_acesso', methods=['POST', 'GET'])
        def primeiro_acesso():
            # abaixo metodo get que renderiza pagina de primeiro acesso
            if request.method == "GET":
                return render_template('primeiro_acesso.html')

            # abaixo é para quando o usuário enviar os dados,
            # isso fará um insert no responsável e no aluno.
            if request.method == "POST":
                # pega todos os dados q o aluno digitou
                nome = str(request.form['nome'])
                sangue = str(request.form['sangue'])
                mao = str(request.form['mao'])
                data = request.form['data']
                senha = generate_password_hash(request.form['senha'])
                nme_r = str(request.form['nme_r'])
                cpf = (request.form['cpf'])

                # abre o banco de dados e inicia uma transação, insere o resp.
                # e depois o aluno, em seguida é feito um commit para cumprir os
                # dois inserts, caso falhe em um os dois processos não se completam
                mysql = bd.SQL()
                mysql.cnx.start_transaction()
                comando = "INSERT INTO tb_responsavel(cpf_responsavel, nme_responsavel) " \
                          "VALUES(%s, %s);"
                cs1 = mysql.executar(comando, [cpf, nme_r])

                comando = "INSERT INTO tb_aluno(nme_aluno, senha_aluno, " \
                          "nasc_aluno, mao_aluno, sangue_aluno, cod_aluno_resp) " \
                          "VALUES(%s, %s, %s, %s, %s, %s);"
                cs2 = mysql.executar(comando, [nome, senha, data, mao, sangue, cpf])
                mysql.cnx.commit()

                # abaixo existem mensagens de sucesso ou erro para exibir ao usuario
                if cs1 and cs2:
                    msg = 'Sucesso ao cadastrar'
                    return msg
                else:
                    msg = 'Falha no cadastro.'
                    return msg
