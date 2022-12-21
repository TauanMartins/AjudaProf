from checar_sessao import *


class Direcao:
    def __init__(self, app):
        # existe um login geral que não
        # é preciso do banco de dados, agilizando o processo de uso/modificação
        @app.route('/login_d', methods=['POST', 'GET'])
        def login_d():
            usuario = "1111111111"
            senha = "ajuda_prof_admin@"
            if request.method == "POST":
                # pega oq o usuario digitou no usuario e senha
                usuario_d = str(request.form['usuario_d'])
                senha_d = str(request.form['senha_d'])

                # se os dados forem compatíveis ao usuário e senha administrativos
                # será permitida a entrada do usuário para o menu principal
                # caso não sejam compatíveis é retornado para tela de login_d
                if usuario != usuario_d or senha != senha_d:
                    return redirect('/login_d')

                # comando que leva para o menu principal
                elif senha == senha_d:
                    session.permanent = True
                    session['user_d'] = usuario_d
                    return redirect('/menu_principal_dir')

            # abaixo um metodo get
            else:
                # if abaixo valida se o usuário ja estava logada na maquina
                # permitindo uma entrada mais rápida.
                if "user_d" in session:
                    return redirect('/menu_principal_dir')
                return render_template('login_d.html')

        @app.route('/menu_principal_dir', methods=['POST', 'GET'])
        @checar_sessao_direcao
        def menu_principal_dir():
            return render_template('menu_dir.html')

        @app.route('/incluir_prof', methods=['POST', 'GET'])
        @checar_sessao_direcao
        def incluir_prof():
            # sel = ''
            # metodo get abaixo renderiza formulario p inclusão de professor
            if request.method == 'GET':
                return render_template('incluir_prof.html')

            # metodo post abaixo puxa todos os dados digitados do professor
            elif request.method == 'POST':
                nme_professor = request.form['nme_professor']
                senha_professor = generate_password_hash(request.form['senha_professor'])
                matricula_professor = request.form['matricula_professor']
                nasc_professor = request.form['date']
                sangue_professor = request.form['sangue_professor']

                # abre o banco para inserir um professor com os dados requisitados
                mysql = db.SQL()
                comando = "INSERT INTO tb_professor(nme_professor, senha_professor, " \
                          "matricula_professor, " \
                          "nasc_professor, sangue_professor) " \
                          "values(%s, %s, %s, %s, %s);"

                mysql.executar(comando, [nme_professor, senha_professor, matricula_professor,
                                         nasc_professor, sangue_professor])
                mysql.cnx.commit()
                return "ok"

        @app.route('/alterar_prof', methods=['POST', 'GET'])
        @checar_sessao_direcao
        def alterar_prof():
            sel = ''
            # metodo get abaixo retorna todos os professores bem como suas disciplinas
            if request.method == "GET":
                # abre o banco de dados para puxar professores
                mysql = db.SQL()
                comando = "SELECT idt_professor, nme_professor, matricula_professor, nasc_professor," \
                          "sangue_professor, nme_disciplina FROM tb_professor join tb_disciplina on " \
                          "cod_disciplina_professor=idt_professor " \
                          "GROUP BY nme_professor, nme_disciplina;"
                cs = mysql.consultar(comando, ())

                # abaixo é tratado todos os professores para serem mostrados na tela
                for [idt_professor, nme_professor, matricula_professor, nasc_professor,
                     sangue_professor, nme_disciplina] in cs:
                    sel += f"""<tr style="height: 43px;">
                                            <td class="u-border-2 u-border-grey-dark-1 u-first-column u-grey-5 u-table-cell">{nme_professor}<br></td>
                                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">********</td>
                                            <td class ="u-border-2 u-border-grey-dark-1 u-table-cell">{matricula_professor}</td>
                                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{nasc_professor} </td>
                                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{sangue_professor} </td>
                                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{nme_disciplina}</td>
                                            <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><button
                                            class="idt" name='idt' id='idt' value="{idt_professor}"
                                            onclick="especificar({idt_professor})" >Alterar</button></td></tr>"""
                return render_template('alterar_prof.html', prof=sel)
            elif request.method == "POST" and request.form.get('matricula') is None:
                idtProfessor = request.form['idt']
                mysql = db.SQL()
                comando = "SELECT * FROM tb_professor join tb_disciplina on cod_disciplina_professor=idt_professor " \
                          "WHERE idt_professor=%s GROUP BY nme_professor;"
                cs = mysql.consultar(comando, [int(idtProfessor)])

                for [idt_professor, nme_professor, senha_professor, matricula_professor, nasc_professor,
                     sangue_professor,
                     idt_disciplina, nme_disciplina, cod_disciplina_professor, cod_disciplina_serie] in cs:
                    selectSangue = f"""<select id="sangue" name="sangue" type="text">
                                                                <option value="{sangue_professor}">Sangue</option>
                                                              <option value="A+">A+</option>
                                                              <option value="A-">A-</option>
                                                              <option value="B+">B+</option>
                                                              <option value="B-">B-</option>
                                                              <option value="AB+">AB+</option>
                                                              <option value="AB-">AB-</option>
                                                              <option value="O+">O+</option>
                                                              <option value="O-">O-</option> """
                    sel += f"""<tr style="height: 43px;">
                                                <td class="u-border-2 u-border-grey-dark-1 u-first-column u-grey-5 u-table-cell">
                                                <input style="width:110px;" id="nome" name="nome" type="text" value="{nme_professor}"/></td>
                                                <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><input style="width:110px;"
                                                placeholder="Senha" name="senha" id='senha' type="text" minlength='6' maxlength="8"
                                                required="required" value="{senha_professor}" onfocus=""/></td><td
                                                class ="u-border-2 u-border-grey-dark-1 u-table-cell"><input style="width:110px;"
                                                name="matricula" id='matricula' type="text" minlength='10' maxlength="10"
                                                required="required" value="{matricula_professor}"/></td><td
                                                class="u-border-2 u-border-grey-dark-1 u-table-cell"><input style="width:143px;"
                                                name="data" id='data' type="date" value="{nasc_professor}" /></td><td
                                                class="u-border-2 u-border-grey-dark-1 u-table-cell">{selectSangue}</select></td>
                                                <td class="u-border-2 u-border-grey-dark-1 u-table-cell">Todas</td>
                                                <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><button name='idt'
                                                id='idt' value="{idtProfessor}" onclick="alterar({idtProfessor})">Alterar</button></td></tr>"""
                return sel
            elif request.method == "POST" and request.form.get('matricula') is not None:
                idtProfessor = request.form['idt']
                nme = request.form["nome"]
                senha = generate_password_hash(request.form["senha"])
                matricula = request.form["matricula"]
                data = request.form["data"]
                sangue = request.form["sangue"]
                mysql = db.SQL()
                comando = "UPDATE tb_professor SET nme_professor=%s, matricula_professor=%s, senha_professor=%s, " \
                          "nasc_professor=%s, sangue_professor=%s WHERE idt_professor=%s;"
                mysql.executar(comando, [nme, matricula, senha, data, sangue, idtProfessor])
                mysql.cnx.commit()
                return "alterou"

        @app.route('/matricular_aluno', methods=['POST', 'GET'])
        @checar_sessao_direcao
        def matricular_aluno():
            sel = ''
            # metodo get que renderiza a pagina de matricular aluno
            if request.method == 'GET':
                return render_template('matricular_aluno.html', aluno=sel)
            # metodo post para caso aperte mostrar alunos,
            # mostre todos os alunos não matriculados
            if request.method == "POST" and request.form.get('idt') is None:
                # abre o banco de dados para mostrar os alunos
                mysql = db.SQL()
                comando = "SELECT * FROM tb_aluno join tb_responsavel on cod_aluno_resp=cpf_responsavel " \
                          "WHERE matricula_aluno is NULL ORDER BY nme_aluno;"
                cs = mysql.consultar(comando, ())

                # abaixo é tratados todos os alunos para mostrar na tela
                for [idt_aluno, nme_aluno, senha_aluno, matricula_aluno, nasc_aluno, mao_aluno, sangue_aluno,
                     cod_aluno_serie, cod_responsavel, cpf_responsavel, nme_responsavel] in cs:
                    sel += f"""<tr style="height: 43px;">
                                                    <td class="u-border-2 u-border-grey-dark-1 u-first-column u-grey-5 u-table-cell">
                                                    {nme_aluno}<br></td><td class="u-border-2 u-border-grey-dark-1 u-table-cell">NULO</td>
                                                    <td class ="u-border-2 u-border-grey-dark-1 u-table-cell">{nasc_aluno}</td>
                                                    <td class="u-border-2 u-border-grey-dark-1 u-table-cell">NULO</td>
                                                    <td class="u-border-2 u-border-grey-dark-1 u-table-cell">NULO</td>
                                                    <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{mao_aluno}</td>
                                                    <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{sangue_aluno}</td>
                                                    <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{nme_responsavel}</td>
                                                    <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><button
                                                    class="idt" name='idt' id='idt' value="{idt_aluno}" onclick="especificar({idt_aluno})" >
                                                    Matricular</button></td></tr>"""
                return sel

            # condição para que mostre o aluno escolhido para a matrícula
            # podendo assim editar informações erradas e matricular
            elif request.method == "POST" and request.form.get('serie') is None:
                # requere informação daquele usuario clicado para mostrá-lo
                idtAluno = request.form["idt"]

                # abre o banco de dados e puxa aquele aluno especifico
                mysql = db.SQL()
                comando = "SELECT * FROM tb_aluno join tb_responsavel on cod_aluno_resp=cpf_responsavel WHERE idt_aluno=%s;"
                cs = mysql.consultar(comando, ([idtAluno]))

                # abaixo é tratado o aluno para aparecer na tela
                for [idt_aluno, nme_aluno, senha_aluno, matricula_aluno, nasc_aluno, mao_aluno,
                     sangue_aluno, cod_turma, cod_responsavel, cpf_responsavel, nme_responsavel] in cs:
                    selectSerie = """<select name="serie" id="serie" autofocus="autofocus"
                                                        class="u-border-1 u-border-grey-30 u-input u-input-rectangle">
                                                                                  <option value="0">Série</option>
                                                                                  <option value="6">6º ano</option>
                                                                                  <option value="7">7º ano</option>
                                                                                  <option value="8">8º ano</option>
                                                                                  <option value="9">9º ano</option>
                                                                                  <option value="1">1º ano</option>
                                                                                  <option value="2">2º ano</option>
                                                                                  <option value="3">3º ano</option>
                                                                                """
                    selectTurma = """<select id="turma" name="turma"
                                                            class="u-border-1 u-border-grey-30 u-input u-input-rectangle u-white">
                                                                            <optionvalue="A">Turma</option>
                                                                            <option value="A">A</option>"""
                    sel += f"""<tr style="height: 43px;">
                                                        <td class="u-border-2 u-border-grey-dark-1 u-first-column
                                                        u-grey-5 u-table-cell"><input id="nome" name="nome" type="text"
                                                        value="{nme_aluno}"/><br></td><td class="u-border-2 u-border-grey-dark-1
                                                        u-table-cell"><input name="matricula" id='matricula' type="text"
                                                        minlength='10' maxlength="10" required="required" value="{matricula_aluno}"/></td>
                                                        <td class ="u-border-2 u-border-grey-dark-1 u-table-cell">
                                                        <input name="data" id='data' type="date" value="{nasc_aluno}" /></td>
                                                        <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{selectSerie} /></td>
                                                        <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{selectTurma} /></td>
                                                        <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{mao_aluno}</td>
                                                        <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{sangue_aluno}</td>
                                                        <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{nme_responsavel}</td>
                                                        <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><button name='idt'
                                                        id='idt' value="{idtAluno}" onclick="matricular({idtAluno})" >Matricular</button></td></tr>"""
                return sel

            # condição para matricular o aluno e jogar no banco de dados
            elif request.method == "POST" and request.form.get('serie') is not None:
                # puxa todos os dados digitados pelo usuário
                idtAluno = request.form['idt']
                nme = request.form["nome"]
                matricula = request.form["matricula"]
                serie = request.form["serie"]

                # abre o banco de dados e faz o update com dados requisitados
                mysql = db.SQL()
                comando2 = "UPDATE tb_aluno SET nme_aluno=%s, matricula_aluno=%s, " \
                           "cod_aluno_serie=%s WHERE idt_aluno=%s;"
                mysql.executar(comando2, [nme, matricula, serie, idtAluno])
                mysql.cnx.commit()
                return "ok"

        @app.route('/alterar_aluno', methods=['POST', 'GET'])
        @checar_sessao_direcao
        def alterar_aluno():
            sel = ''
            # metodo get que renderiza a pagina de alterar aluno
            if request.method == 'GET':
                return render_template('alterar_aluno.html', aluno=sel)
            # metodo post para mostrar todos os alunos da turma especificada
            if request.method == "POST" and request.form.get('idt') is None:
                # puxa os dados da serie selecionada
                idtSerie = request.form['select']

                # abre o banco de dados para puxar todos os alunos
                mysql = db.SQL()
                comando = "SELECT * FROM tb_aluno JOIN tb_turma ON idt_serie_turma=cod_aluno_serie " \
                          "AND idt_serie_turma=%s ORDER BY nme_aluno;"
                cs = mysql.consultar(comando, ([idtSerie]))

                # é tratado todos os alunos para aparecerem na tela
                for [idt_aluno, nme_aluno, senha_aluno, matricula_aluno, nasc_aluno, mao_aluno,
                     sangue_aluno, cod_turma, cod_responsavel, idt_serie_turma, turma] in cs:
                    sel += f"""<tr style="height: 43px;">
                                                    <td class="u-border-2 u-border-grey-dark-1 u-first-column u-grey-5 u-table-cell">{nme_aluno}<br></td>
                                                    <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{matricula_aluno}</td>
                                                    <td class ="u-border-2 u-border-grey-dark-1 u-table-cell">{nasc_aluno}</td>
                                                    <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{idt_serie_turma}º ano </td>
                                                    <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{turma} </td>
                                                    <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{mao_aluno}</td>
                                                    <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{sangue_aluno}</td>
                                                    <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><button class="idt"
                                                    name='idt' id='idt' value="{idt_aluno}" onclick="especificar({idt_aluno})" >Alterar</button></td></tr>"""
                return sel

            # metodo post para mostrar aquele aluno específico
            elif request.method == "POST" and request.form.get('matricula') is None:
                # puxa os dados do aluno específico
                idtAluno = request.form['idt']

                # abre o banco para puxar dados daquele aluno específico
                mysql = db.SQL()
                comando = "SELECT * FROM tb_aluno JOIN tb_turma ON " \
                          "idt_serie_turma=cod_aluno_serie WHERE idt_aluno=%s;"
                cs = mysql.consultar(comando, [int(idtAluno)])

                # é tratado o aluno para ser mostrado na tela
                for [idt_aluno, nme_aluno, senha_aluno, matricula_aluno, nasc_aluno, mao_aluno,
                     sangue_aluno, cod_turma, cod_responsavel, idt_serie_turma, turma] in cs:
                    selectSerie = f"""<select name="serie" id="serie" autofocus="autofocus"
                                                             class="u-border-1 u-border-grey-30 u-input u-input-rectangle">
                                                                          <option value="{idt_serie_turma}">Série/Ano</option>
                                                                          <option value="6">6º ano</option>
                                                                          <option value="7">7º ano</option>
                                                                          <option value="8">8º ano</option>
                                                                          <option value="9">9º ano</option>
                                                                          <option value="1">1º ano</option>
                                                                          <option value="2">2º ano</option>
                                                                          <option value="3">3º ano</option>
                                                                        """
                    selectSangue = f"""<select id="sangue" name="sangue" type="text"
                                                                    class="u-border-1 u-border-grey-30 u-input u-input-rectangle u-white">
                                                                  <option value="{sangue_aluno}">Sangue</option>
                                                                  <option value="A+">A+</option>
                                                                  <option value="A-">A-</option>
                                                                  <option value="B+">B+</option>
                                                                  <option value="B-">B-</option>
                                                                  <option value="AB+">AB+</option>
                                                                  <option value="AB-">AB-</option>
                                                                  <option value="O+">O+</option>
                                                                  <option value="O-">O-</option> """
                    selectTurma = f"""<select id="turma" name="turma"
                                                class="u-border-1 u-border-grey-30 u-input u-input-rectangle u-white">
                                                                        <optionvalue="{turma}">Turma</option>
                                                                        <option value="A">A</option>
                                                                        <option value="B">B</option>
                                                                        <option value="C">C</option>"""
                    selectMao = f"""<select id="select-ab6a" name="mao"
                                            class="u-border-1 u-border-grey-30 u-input u-input-rectangle u-white">
                                                                <option value="{mao_aluno}">Mão</option>
                                                                <option value="destro">Destro</option>
                                                                <option value="canhoto">Canhoto</option>
                                                                <option value="ambidestro">Ambidestro</option>"""
                    sel += f"""<tr style="height: 43px;">
                                                    <td class="u-border-2 u-border-grey-dark-1 u-first-column u-grey-5 u-table-cell">
                                                    <input id="nome" name="nome" type="text" value="{nme_aluno}"/><br></td>
                                                    <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><input name="matricula"
                                                    id='matricula' type="text" minlength='10' maxlength="10" required="required" value="{matricula_aluno}"/></td>
                                                    <td class ="u-border-2 u-border-grey-dark-1 u-table-cell">
                                                    <input name="data" id='data' type="date" value="{nasc_aluno}" /></td>
                                                    <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{selectSerie} /></td>
                                                    <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{selectTurma} /></td>
                                                    <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{selectMao}/></td>
                                                    <td class="u-border-2 u-border-grey-dark-1 u-table-cell">{selectSangue}/></td>
                                                    <td class="u-border-2 u-border-grey-dark-1 u-table-cell"><button
                                                    name='idt' id='idt' value="{idtAluno}" onclick="alterar({idt_aluno})" >Alterar</button></td></tr>"""
                return sel

            # metodo get abaixo faz o update no banco
            elif request.method == "POST" and request.form.get('matricula') is not None:
                # requisita todos os dados para alteração
                idtAluno = request.form['idt']
                nme = request.form["nome"]
                matricula = request.form["matricula"]
                serie = request.form["serie"]
                # turma = request.form["turma"]
                data = request.form["data"]
                mao = request.form["mao"]
                sangue = request.form["sangue"]

                # abre o banco e faz o update no aluno de acordo as info requisitadas
                mysql = db.SQL()
                comando = "UPDATE tb_aluno SET nme_aluno=%s, matricula_aluno=%s, " \
                          "nasc_aluno=%s, mao_aluno=%s, sangue_aluno=%s, cod_aluno_serie=%s WHERE idt_aluno=%s;"
                mysql.executar(comando, [nme, matricula, data, mao, sangue, serie, idtAluno])
                mysql.cnx.commit()
                return "ok"

        @app.route('/incluir_disc', methods=['POST', 'GET'])
        @checar_sessao_direcao
        def incluir_disc():
            # metodo get abaixo renderiza a tela junto com os professores que ali existem
            if request.method == 'GET':
                # abre o banco de dados e puxa todos os professores
                mysql = db.SQL()
                comando = "SELECT idt_professor, nme_professor FROM tb_professor ORDER BY nme_professor;"
                cs = mysql.consultar(comando, ())
                # é tratado os profs para serem inseridos no select
                sel = f"""<select id="select-20fa" name="nme_professor"
                                                    class="u-border-1 u-border-grey-30 u-input u-input-rectangle u-white" >
                                                    <option value="{0}">Professor</option>"""
                for [idt_professor, nme_professor] in cs:
                    sel += f"""<option value="{idt_professor}">{nme_professor}</option> """
                sel += "</select>"

                # comando para mostrar todas as turmas que existem
                comando2 = "SELECT idt_serie_turma FROM tb_turma ORDER BY idt_serie_turma;"
                cs2 = mysql.consultar(comando2, ())

                # é tratado todas turmas para serem mostradas na tela
                sel2 = f"""<select id="select-20fa" name="serie"
                                                    class="u-border-1 u-border-grey-30 u-input u-input-rectangle u-white" >
                                                    <option value="{0}">Série/Ano</option>"""
                for [idt_serie_turma] in cs2:
                    sel2 += f"""<option value="{idt_serie_turma}">{idt_serie_turma}º Ano</option> """
                sel2 += "</select>"

                return render_template('incluir_disc.html', nme_professor=sel, idt_serie=sel2)

            # metodo post para ser inserido a disciplina juntamente com as avaliações
            if request.method == 'POST':
                # comandos para puxar os dados inseridos
                nme_disciplina = request.form['disciplina']
                idt_professor = request.form['nme_professor']
                idt_serie = request.form['serie']
                peso1 = request.form['peso1']
                peso2 = request.form['peso2']
                peso3 = request.form['peso3']
                peso4 = request.form['peso4']

                # abre o banco e inicia uma transação
                mysql = db.SQL()
                mysql.cnx.start_transaction()

                # insere uma disciplina na tabela de acordo com as informações dadas
                comando0 = "INSERT INTO tb_disciplina(nme_disciplina, cod_disciplina_serie, " \
                           "cod_disciplina_professor) values(%s, %s, %s);"
                mysql.executar(comando0, [nme_disciplina, idt_serie, idt_professor])

                # comando abaixo mostra o idt da disciplina que acaba de ser criada
                # para assim ser inseridas as avaliações de cada bimestre
                comando1 = "SELECT idt_disciplina FROM tb_disciplina " \
                           "JOIN tb_turma on idt_serie_turma=cod_disciplina_serie " \
                           "WHERE nme_disciplina=%s and cod_disciplina_serie=%s;"
                cs = mysql.consultar(comando1, [nme_disciplina, idt_serie])
                dados = cs.fetchone()

                # comando abaixo insere as avaliações de todos os bimestres junto com seus pesos
                comando1 = "INSERT INTO tb_avaliacao(peso_avaliacao, cod_avaliacao_disciplina, " \
                           "cod_avaliacao_serie, cod_avaliacao_bimestre) " \
                           "values(%s, %s, %s, %s),(%s, %s, %s, %s),(%s, %s, %s, %s),(%s, %s, %s, %s);"
                mysql.executar(comando1, [peso1, dados[0], idt_serie, 1, peso2, dados[0],
                                          idt_serie, 2, peso3, dados[0], idt_serie, 3, peso4, dados[0], idt_serie, 4])

                # comando para fechar a transação e se correr td bem os dois comandos
                # inserem disciplina e avaliações
                mysql.cnx.commit()
                return "ok"
            return render_template('incluir_disc.html')

        @app.route('/incluir_avaliacao', methods=['POST', 'GET'])
        @checar_sessao_direcao
        def incluir_avaliacao():
            sel = ''
            disc = ''
            # abaixo há um comando get que mostra todos as disciplinas e anos para matricular
            # o boletim dos alunos que posteriormente aparecerão
            if request.method == 'GET':
                # abre o banco de dados para mostrar todas as disciplinas e series
                # para formar o select
                mysql = db.SQL()
                comando0 = "SELECT idt_disciplina, nme_disciplina, cod_disciplina_serie FROM tb_disciplina " \
                           "JOIN tb_turma on idt_serie_turma=cod_disciplina_serie ORDER BY nme_disciplina;"
                cs = mysql.consultar(comando0, ())

                # abaixo são tratadas as informações para aparecerem na tela
                for [idt_disciplina, nme_disciplina, serie] in cs:
                    disc += f"""<option value="{idt_disciplina}" >{nme_disciplina} - {serie}º Ano</option> """
                return render_template('incluir_avaliacao.html', disciplina=disc)

            # metodo post abaixo para mostrar todos os alunos da disciplina e serie especificadas
            elif request.method == 'POST' and request.form.get("idt_aluno") is None:
                # puxa o idt da disciplina indicada
                idt_disciplina = request.form['idt_disciplina']

                # abre o banco para mostrar alunos daquela serie e disciplina
                # que não possuem boletim cadastrados
                mysql = db.SQL()
                comando = "SELECT idt_aluno, nme_aluno, cod_avaliacao_serie, cod_avaliacao_disciplina FROM " \
                          "(select idt_aluno, nme_aluno, cod_avaliacao_serie, cod_avaliacao_disciplina " \
                          "FROM tb_avaliacao JOIN tb_aluno ON cod_avaliacao_serie=cod_aluno_serie WHERE cod_avaliacao_disciplina=%s) c1 " \
                          "LEFT JOIN (SELECT cod_notas_aluno FROM tb_notas JOIN tb_avaliacao " \
                          "ON cod_notas_avaliacao=idt_avaliacao WHERE cod_avaliacao_disciplina=%s) c2 " \
                          "ON c1.idt_aluno=c2.cod_notas_aluno WHERE c2.cod_notas_aluno IS NULL GROUP BY idt_aluno;"
                cs = mysql.consultar(comando, [idt_disciplina, idt_disciplina])
                if not cs:
                    return sel
                # abaixo é tratado as informações para aparecerem na tela
                for [idt_aluno, nme_aluno, serie, idt_disciplina] in cs:
                    sel += f"""<tr style="height: 43px;">
                                                    <td class="u-border-2 u-border-grey-dark-1 u-first-column u-grey-5 u-table-cell">{nme_aluno}<br></td>
                                                    <td class ="u-border-2 u-border-grey-dark-1 u-table-cell">{serie}º Ano</td>
                                                    <input type="hidden" id="idt_aluno" value="{idt_aluno}"/>
                                                    <input type="hidden" id="idt_disciplina" value="{idt_disciplina}"/></tr>"""
                return sel

            # metodo post para matricular boletins dos alunos que nao tinham
            if request.method == "POST":
                # puxa o idt da disciplina especificada antes
                idt_disciplina = int(request.form['idt_disciplina'])

                # abre o banco de dados e inicia uma transação, em seguida é mostrado todos
                # os alunos que nao tem boletim cadastrados daquela disciplina/serie
                mysql0 = db.SQL()
                mysql0.cnx.start_transaction()
                comando1 = "SELECT idt_aluno, idt_avaliacao FROM " \
                           "(select idt_aluno, idt_avaliacao, cod_avaliacao_bimestre " \
                           "FROM tb_avaliacao JOIN tb_aluno ON cod_avaliacao_serie=cod_aluno_serie WHERE cod_avaliacao_disciplina=%s) c1 " \
                           "LEFT JOIN (SELECT cod_notas_aluno FROM tb_notas JOIN tb_avaliacao " \
                           "ON cod_notas_avaliacao=idt_avaliacao WHERE cod_avaliacao_disciplina=%s) c2 " \
                           "ON c1.idt_aluno=c2.cod_notas_aluno WHERE c2.cod_notas_aluno IS NULL;"
                cs = mysql0.consultar(comando1, [idt_disciplina, idt_disciplina])

                # caso não tenha alunos e usuário mesmo assim clicou em inserir é retornado nada para o usuário
                if not cs:
                    return sel

                # insere o boletim apenas para aqueles alunos mostrados
                comando2 = "INSERT INTO tb_notas(cod_notas_aluno, cod_notas_avaliacao) VALUES"
                for [idt_aluno, idt_avaliacao] in cs:
                    if cs is None:
                        return "ok"
                    comando2 += f"({idt_aluno}, {idt_avaliacao}),"
                # comandos para retirar a última vírgula e coloca um ; pra nao haver conflito
                comando2 = comando2[:-1]
                comando2 += ";"

                # ultimas duas linhas executa o comando de inserir e fecha a transação
                mysql0.executar(comando2, [])
                mysql0.cnx.commit()

                return "ok"
