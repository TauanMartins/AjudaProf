


select * from tb_turma;
select * from tb_bimestre;
select * from ta_bimestre_turma order by cod_bimestre;

/*/ comando abaixo faz parte do menu da direçao para incluir uma avaliacao e jogar p todos os alunos/*/
INSERT into tb_avaliacao(dt_avaliacao, cod_disciplina, cod_avaliacao_turma, cod_bimestre) values (20210630, 3, 6, 3);
/*/ comando abaixo mostra todos os alunos daquela serie para jogar a avaliacao/*/
select idt_aluno, nme_aluno from tb_aluno join tb_turma on tb_aluno.cod_turma=tb_turma.idt_serie_turma where idt_serie_turma=6;
/*/ comando abaixo insere os boletins dos alunos daquela avaliacao da disciplina e serie especificados/*/
insert into tb_notas(cod_aluno, cod_avaliacao) values(1,15);

/*/ comando abaixo mostra todos os alunos e notas daquele professor, disciplina e serie especificados/*/
SELECT idt_aluno, nme_aluno, n1, n2, n3, media, rec, idt_notas,
cod_avaliacao_serie, peso_avaliacao FROM tb_aluno JOIN tb_notas 
JOIN tb_avaliacao JOIN ta_bimestre_turma JOIN tb_disciplina 
ON cod_aluno_serie=cod_ta_serie_turma AND cod_notas_aluno=idt_aluno 
AND cod_notas_avaliacao=idt_avaliacao AND 
cod_avaliacao_bimestre=cod_ta_bimestre AND
cod_avaliacao_serie=cod_ta_serie_turma AND 
cod_avaliacao_disciplina=idt_disciplina WHERE cod_ta_bimestre=1 
AND cod_ta_serie_turma=6 AND idt_disciplina=24;

/*/ abaixo mostra a presenca do aula a partir dos filtros/*/
SELECT distinct idt_aluno, nme_aluno, presen_aula FROM tb_aluno JOIN tb_aula JOIN tb_turma JOIN tb_aula_aluno JOIN tb_disciplina 
JOIN ta_bimestre_turma JOIN tb_bimestre ON tb_aluno.idt_aluno=tb_aula_aluno.cod_aluno_aula AND tb_aula_aluno.cod_aula=tb_aula.idt_aula 
AND tb_aluno.cod_turma=tb_turma.idt_serie_turma AND tb_turma.idt_serie_turma=ta_bimestre_turma.cod_serie_turma AND 
tb_bimestre.idtb_bimestre=ta_bimestre_turma.cod_bimestre AND tb_aula.cod_bimestre_aula=ta_bimestre_turma.cod_bimestre AND tb_aula.cod_turma=idt_serie_turma 
AND tb_disciplina.cod_disciplina_turma=tb_turma.idt_serie_turma WHERE tb_aula.cod_bimestre_aula=1 AND idt_serie_turma=6 AND idt_disciplina=1 ;

SELECT idt_aluno, nme_aluno, presen_aula, conteudo_aula, idt_aula FROM tb_aluno 
JOIN ta_aula_aluno JOIN tb_aula JOIN ta_bimestre_turma JOIN tb_disciplina 
ON idt_aluno=cod_ta_aluno AND idt_aula=cod_ta_aula AND 
cod_ta_serie_turma=cod_aula_serie AND cod_aula_disciplina=idt_disciplina 
AND cod_aula_bimestre=cod_ta_bimestre WHERE tb_aula.cod_aula_bimestre=1 
AND cod_ta_serie_turma=6 AND idt_disciplina=24 and dt_aula=20210716 ORDER BY nme_aluno;


SELECT idt_serie_turma, cod_bimestre, nme_disciplina, idt_avaliacao from tb_turma JOIN tb_avaliacao JOIN ta_bimestre_turma JOIN tb_bimestre JOIN tb_disciplina
 WHERE tb_avaliacao.cod_avaliacao_turma=idt_serie_turma and tb_avaliacao.cod_disciplina=idt_disciplina and
 idt_serie_turma=cod_serie_turma and idtb_bimestre=cod_bimestre and idt_serie_turma=cod_disciplina_turma;


select * from tb_aula;
insert into tb_aula(dt_aula, conteudo_aula, cod_aula_disciplina, cod_aula_bimestre, cod_aula_serie)
values(20210716, "Baskhara", 24, 1, 6);
select * from ta_aula_aluno;
insert into ta_aula_aluno(cod_ta_aula, cod_ta_aluno) values(1, 1),(1, 2),(1, 3), (1, 9);


/*/ comando abaixo mostra todos os professores de todas as turmas/*/
SELECT * FROM tb_professor join tb_disciplina on cod_disciplina_professor=idt_professor ORDER BY nme_professor;

/*/ comando abaixo lista todas as disciplinas de todas as séries daquele professor especificado/*/
select idt_disciplina, nme_disciplina, cod_disciplina_serie as Serie from tb_disciplina join tb_professor on idt_professor=cod_disciplina_professor;

/*/ comando abaixo lista todos os alunos na escola e de que ano eles são /*/
SELECT * FROM tb_aluno JOIN tb_turma ON idt_serie_turma=cod_turma ORDER BY nme_aluno;


show tables;
describe ta_bimestre_turma;
select * from tb_avaliacao;
delete from tb_avaliacao where idt_avaliacao=26;

delete from ta_bimestre_turma;
delete from ta_mensagem;
delete from tb_aula;
delete from tb_bimestre;
delete from tb_disciplina;
delete from tb_notas;
delete from tb_turma;
delete from tb_avaliacao;
delete from tb_aluno;
delete from tb_professor;
delete from tb_responsavel;

	
drop table if exists ta_mensagem;
drop table if exists tb_aula;
drop table if exists tb_bimestre;
drop table if exists tb_disciplina;
drop table if exists tb_notas;
drop table if exists tb_turma;
drop table if exists tb_avaliacao;
drop table if exists tb_aluno;
drop table if exists tb_professor;
drop table if exists tb_responsavel;


select * from tb_turma;

select * from tb_professor;
insert into tb_professor(nme_professor, senha_professor, matricula_professor, nasc_professor, sangue_professor) 
values("Fabiano", "senha123", "1234567891", 19980122, "A+");

select * from tb_disciplina;
insert into tb_disciplina(nme_disciplina, cod_turma, cod_professor) values("Português", 7, 2);

select * from tb_aluno;

select * from tb_avaliacao;
insert into tb_avaliacao(dt_avaliacao, cod_turma, cod_disciplina) values(20210731, 6, 1);
update tb_avaliacao set nme_avaliacao="N2" where idt_avaliacao=4; 

select n1, n2, n3, cod_aluno, cod_avaliacao, idt_notas from tb_notas where idt_notas=16;
insert into tb_notas(aluno_notas,cod_aluno, cod_avaliacao) values(2.75,2, 4);
update tb_notas set aluno_notas=4 where cod_aluno=2 and cod_avaliacao=2;
delete from tb_notas where idt_notas=25;

select tb_aluno.nme_aluno as Aluno, nme_avaliacao as Avaliacao, tb_notas.aluno_notas as Nota from tb_aluno JOIN tb_notas
JOIN tb_disciplina JOIN tb_avaliacao JOIN tb_turma ON tb_notas.cod_aluno=tb_aluno.idt_aluno AND tb_disciplina.idt_disciplina=tb_avaliacao.cod_disciplina
AND tb_avaliacao.idt_avaliacao=tb_notas.cod_avaliacao AND  tb_turma.idt_serie_turma=tb_avaliacao.cod_turma AND tb_turma.idt_serie_turma=tb_aluno.cod_turma
AND tb_turma.idt_serie_turma=tb_disciplina.cod_turma where nme_disciplina="Matemática" AND bimestre_turma=1 order by nme_aluno, idt_notas;
/*/ primeira condicao limita a mostrar alunos que possuem apenas aquelas notas ligadas à eles, a segunda condicao limita a mostrar apenas as disciplinas
que são ligadas aquela avaliacao especifica, terceira condicao limita mostrar dados da avaliacao que são ligados àquelas notas, as três condições seguintes
referem-se somente a mostrar todos os dados daquele bimestre especificado 
for[nme_aluno, n1, n2, n3] in cs:
	aluno=nme_aluno
	nota=n1
	nota=n2
    nota=n3
/*/
