-- -----------------------------------------------------
-- Table `tb_bimestre`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tb_bimestre` (
  `idtb_bimestre` INT(11) NOT NULL,
  PRIMARY KEY (`idtb_bimestre`),
  UNIQUE INDEX `idtb_bimestre_UNIQUE` (`idtb_bimestre` ASC) VISIBLE);




-- -----------------------------------------------------
-- Table `tb_turma`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tb_turma` (
  `idt_serie_turma` INT(11) NOT NULL,
  `turma` VARCHAR(1) NOT NULL,
  PRIMARY KEY (`idt_serie_turma`));




-- -----------------------------------------------------
-- Table `ta_bimestre_turma`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ta_bimestre_turma` (
  `cod_ta_bimestre` INT(11) NOT NULL,
  `cod_ta_serie_turma` INT(11) NOT NULL,
  PRIMARY KEY (`cod_ta_bimestre`, `cod_ta_serie_turma`),
  INDEX `fk_tb_bimestre_has_tb_turma_tb_turma1_idx` (`cod_ta_serie_turma` ASC) VISIBLE,
  INDEX `fk_tb_bimestre_has_tb_turma_tb_bimestre1_idx` (`cod_ta_bimestre` ASC) VISIBLE,
  CONSTRAINT `fk_tb_bimestre_has_tb_turma_tb_bimestre1`
    FOREIGN KEY (`cod_ta_bimestre`)
    REFERENCES `tb_bimestre` (`idtb_bimestre`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_bimestre_has_tb_turma_tb_turma1`
    FOREIGN KEY (`cod_ta_serie_turma`)
    REFERENCES `tb_turma` (`idt_serie_turma`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);




-- -----------------------------------------------------
-- Table `tb_responsavel`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tb_responsavel` (
  `cpf_responsavel` CHAR(12) NOT NULL,
  `nme_responsavel` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`cpf_responsavel`));




-- -----------------------------------------------------
-- Table `tb_aluno`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tb_aluno` (
  `idt_aluno` INT(11) NOT NULL AUTO_INCREMENT,
  `nme_aluno` VARCHAR(45) NOT NULL,
  `senha_aluno` VARCHAR(128) NOT NULL,
  `matricula_aluno` CHAR(11) NULL DEFAULT NULL,
  `nasc_aluno` DATE NOT NULL,
  `mao_aluno` VARCHAR(10) NOT NULL,
  `sangue_aluno` CHAR(3) NOT NULL,
  `cod_aluno_serie` INT(11) NULL DEFAULT NULL,
  `cod_aluno_resp` CHAR(12) NOT NULL,
  PRIMARY KEY (`idt_aluno`),
  UNIQUE INDEX `matricula_aluno_UNIQUE` (`matricula_aluno` ASC) VISIBLE,
  INDEX `fk_tb_aluno_tb_responsavel1_idx` (`cod_aluno_resp` ASC) VISIBLE,
  INDEX `fk_tb_aluno_ta_bimestre_turma1_idx` (`cod_aluno_serie` ASC) VISIBLE,
  CONSTRAINT `fk_tb_aluno_ta_bimestre_turma1`
    FOREIGN KEY (`cod_aluno_serie`)
    REFERENCES `ta_bimestre_turma` (`cod_ta_serie_turma`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_aluno_tb_responsavel1`
    FOREIGN KEY (`cod_aluno_resp`)
    REFERENCES `tb_responsavel` (`cpf_responsavel`));




-- -----------------------------------------------------
-- Table `tb_professor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tb_professor` (
  `idt_professor` INT(11) NOT NULL AUTO_INCREMENT,
  `nme_professor` VARCHAR(45) NOT NULL,
  `senha_professor` VARCHAR(128) NOT NULL,
  `matricula_professor` CHAR(11) NOT NULL,
  `nasc_professor` DATE NOT NULL,
  `sangue_professor` VARCHAR(3) NOT NULL,
  PRIMARY KEY (`idt_professor`),
  UNIQUE INDEX `matricula_professor_UNIQUE` (`matricula_professor` ASC) VISIBLE);




-- -----------------------------------------------------
-- Table `tb_disciplina`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tb_disciplina` (
  `idt_disciplina` INT(11) NOT NULL AUTO_INCREMENT,
  `nme_disciplina` VARCHAR(45) NOT NULL,
  `cod_disciplina_professor` INT(11) NOT NULL,
  `cod_disciplina_serie` INT(11) NOT NULL,
  PRIMARY KEY (`idt_disciplina`),
  INDEX `fk_tb_disciplina_tb_professor1_idx` (`cod_disciplina_professor` ASC) VISIBLE,
  INDEX `fk_tb_disciplina_ta_bimestre_turma1_idx` (`cod_disciplina_serie` ASC) VISIBLE,
  CONSTRAINT `fk_tb_disciplina_ta_bimestre_turma1`
    FOREIGN KEY (`cod_disciplina_serie`)
    REFERENCES `ta_bimestre_turma` (`cod_ta_serie_turma`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_disciplina_tb_professor1`
    FOREIGN KEY (`cod_disciplina_professor`)
    REFERENCES `tb_professor` (`idt_professor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);




-- -----------------------------------------------------
-- Table `tb_aula`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tb_aula` (
  `idt_aula` INT(11) NOT NULL AUTO_INCREMENT,
  `dt_aula` DATE NOT NULL,
  `conteudo_aula` VARCHAR(200) NOT NULL,
  `cod_aula_disciplina` INT(11) NOT NULL,
  `cod_aula_bimestre` INT(11) NOT NULL,
  PRIMARY KEY (`idt_aula`),
  INDEX `fk_tb_aula_tb_disciplina1_idx` (`cod_aula_disciplina` ASC) VISIBLE,
  INDEX `fk_tb_aula_ta_bimestre_turma1_idx` (`cod_aula_bimestre` ASC) VISIBLE,
  CONSTRAINT `fk_tb_aula_ta_bimestre_turma1`
    FOREIGN KEY (`cod_aula_bimestre`)
    REFERENCES `ta_bimestre_turma` (`cod_ta_bimestre`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_aula_tb_disciplina1`
    FOREIGN KEY (`cod_aula_disciplina`)
    REFERENCES `tb_disciplina` (`idt_disciplina`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);




-- -----------------------------------------------------
-- Table `ta_aula_aluno`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ta_aula_aluno` (
  `presen_aula` VARCHAR(45) NOT NULL DEFAULT 'Não alterado',
  `cod_ta_aula` INT(11) NOT NULL,
  `cod_ta_aluno` INT(11) NOT NULL,
  INDEX `fk_ta_aula_alunoT_tb_aula1_idx` (`cod_ta_aula` ASC) VISIBLE,
  INDEX `fk_ta_aula_alunoT_tb_aluno1_idx` (`cod_ta_aluno` ASC) VISIBLE,
  CONSTRAINT `fk_ta_aula_alunoT_tb_aula1`
    FOREIGN KEY (`cod_ta_aula`)
    REFERENCES `tb_aula` (`idt_aula`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ta_aula_alunoT_tb_aluno1`
    FOREIGN KEY (`cod_ta_aluno`)
    REFERENCES `tb_aluno` (`idt_aluno`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);



-- -----------------------------------------------------
-- Table `tb_avaliacao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tb_avaliacao` (
  `idt_avaliacao` INT(11) NOT NULL AUTO_INCREMENT,
  `nme_avaliacao` VARCHAR(45) NULL DEFAULT 'Avaliação',
  `peso_avaliacao` INT(11) NULL DEFAULT '1',
  `cod_avaliacao_bimestre` INT(11) NOT NULL,
  `cod_avaliacao_serie` INT(11) NOT NULL,
  `cod_avaliacao_disciplina` INT(11) NOT NULL,
  PRIMARY KEY (`idt_avaliacao`),
  INDEX `fk_tb_avaliacao_ta_bimestre_turma1_idx` (`cod_avaliacao_bimestre` ASC, `cod_avaliacao_serie` ASC) VISIBLE,
  INDEX `fk_tb_avaliacao_tb_disciplina1_idx` (`cod_avaliacao_disciplina` ASC) VISIBLE,
  CONSTRAINT `fk_tb_avaliacao_ta_bimestre_turma1`
    FOREIGN KEY (`cod_avaliacao_bimestre` , `cod_avaliacao_serie`)
    REFERENCES `ta_bimestre_turma` (`cod_ta_bimestre` , `cod_ta_serie_turma`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_avaliacao_tb_disciplina1`
    FOREIGN KEY (`cod_avaliacao_disciplina`)
    REFERENCES `tb_disciplina` (`idt_disciplina`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);




-- -----------------------------------------------------
-- Table `tb_mural`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tb_mural` (
  `idt_mural` INT(11) NOT NULL AUTO_INCREMENT,
  `mural_mensagem` VARCHAR(120) NOT NULL,
  `data_mensagem` DATE NOT NULL,
  PRIMARY KEY (`idt_mural`));




-- -----------------------------------------------------
-- Table `tb_notas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tb_notas` (
  `idt_notas` INT(11) NOT NULL AUTO_INCREMENT,
  `n1` FLOAT NULL DEFAULT '0',
  `n2` FLOAT NULL DEFAULT '0',
  `n3` FLOAT NULL DEFAULT '0',
  `media` FLOAT NULL DEFAULT '0',
  `rec` FLOAT NULL DEFAULT '0',
  `cod_notas_aluno` INT(11) NOT NULL,
  `cod_notas_avaliacao` INT(11) NOT NULL,
  PRIMARY KEY (`idt_notas`),
  INDEX `fk_tb_notas_tb_aluno1_idx` (`cod_notas_aluno` ASC) VISIBLE,
  INDEX `fk_tb_notas_tb_avaliacao1_idx` (`cod_notas_avaliacao` ASC) VISIBLE,
  CONSTRAINT `fk_tb_notas_tb_aluno1`
    FOREIGN KEY (`cod_notas_aluno`)
    REFERENCES `tb_aluno` (`idt_aluno`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_notas_tb_avaliacao1`
    FOREIGN KEY (`cod_notas_avaliacao`)
    REFERENCES `tb_avaliacao` (`idt_avaliacao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);



-- -----------------------------------------------------
-- Table `tb_ocorrencia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tb_ocorrencia` (
  `idt_ocorrencia` INT NOT NULL,
  `ocorrencia_msg` VARCHAR(256) NOT NULL,
  `cod_ocorrencia_aluno` INT(11) NOT NULL,
  `cod_ocorrencia_prof` INT(11) NOT NULL,
  PRIMARY KEY (`idt_ocorrencia`),
  INDEX `fk_tb_ocorrencia_tb_aluno1_idx` (`cod_ocorrencia_aluno` ASC) VISIBLE,
  INDEX `fk_tb_ocorrencia_tb_professor1_idx` (`cod_ocorrencia_prof` ASC) VISIBLE,
  CONSTRAINT `fk_tb_ocorrencia_tb_aluno1`
    FOREIGN KEY (`cod_ocorrencia_aluno`)
    REFERENCES `tb_aluno` (`idt_aluno`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_ocorrencia_tb_professor1`
    FOREIGN KEY (`cod_ocorrencia_prof`)
    REFERENCES `tb_professor` (`idt_professor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `ta_aula_aluno`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ta_aula_aluno` (
  `presen_aula` VARCHAR(45) NOT NULL DEFAULT 'Não alterado',
  `cod_ta_aula` INT(11) NOT NULL,
  `cod_ta_aluno` INT(11) NOT NULL,
  INDEX `fk_ta_aula_alunoT_tb_aula1_idx` (`cod_ta_aula` ASC) VISIBLE,
  INDEX `fk_ta_aula_alunoT_tb_aluno1_idx` (`cod_ta_aluno` ASC) VISIBLE,
  CONSTRAINT `fk_ta_aula_alunoT_tb_aula1`
    FOREIGN KEY (`cod_ta_aula`)
    REFERENCES `tb_aula` (`idt_aula`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ta_aula_alunoT_tb_aluno1`
    FOREIGN KEY (`cod_ta_aluno`)
    REFERENCES `tb_aluno` (`idt_aluno`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);



-- -----------------------------------------------------
-- Table `ta_mural_professor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ta_mural_professor` (
  `cod_ta_mp_professor` INT(11) NOT NULL,
  `cod_ta_mp_mural` INT(11) NOT NULL,
  PRIMARY KEY (`cod_ta_mp_professor`, `cod_ta_mp_mural`),
  INDEX `fk_tb_professor_has_tb_mural_tb_mural1_idx` (`cod_ta_mp_mural` ASC) VISIBLE,
  INDEX `fk_tb_professor_has_tb_mural_tb_professor1_idx` (`cod_ta_mp_professor` ASC) VISIBLE,
  CONSTRAINT `fk_tb_professor_has_tb_mural_tb_professor1`
    FOREIGN KEY (`cod_ta_mp_professor`)
    REFERENCES `tb_professor` (`idt_professor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_professor_has_tb_mural_tb_mural1`
    FOREIGN KEY (`cod_ta_mp_mural`)
    REFERENCES `tb_mural` (`idt_mural`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);




-- -----------------------------------------------------
-- Table `ta_mural_aluno`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ta_mural_aluno` (
  `cod_ta_ma_aluno` INT(11) NOT NULL,
  `cod_ta_ma_mural` INT(11) NOT NULL,
  PRIMARY KEY (`cod_ta_ma_aluno`, `cod_ta_ma_mural`),
  INDEX `fk_tb_aluno_has_tb_mural_tb_mural1_idx` (`cod_ta_ma_mural` ASC) VISIBLE,
  INDEX `fk_tb_aluno_has_tb_mural_tb_aluno1_idx` (`cod_ta_ma_aluno` ASC) VISIBLE,
  CONSTRAINT `fk_tb_aluno_has_tb_mural_tb_aluno1`
    FOREIGN KEY (`cod_ta_ma_aluno`)
    REFERENCES `tb_aluno` (`idt_aluno`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_aluno_has_tb_mural_tb_mural1`
    FOREIGN KEY (`cod_ta_ma_mural`)
    REFERENCES `tb_mural` (`idt_mural`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


insert into tb_bimestre(idtb_bimestre) values(1), (2), (3), (4);

insert into tb_turma(idt_serie_turma, turma) values(1, "A");
insert into tb_turma(idt_serie_turma, turma) values(2, "A");
insert into tb_turma(idt_serie_turma, turma) values(3, "A");
insert into tb_turma(idt_serie_turma, turma) values(6, "A");
insert into tb_turma(idt_serie_turma, turma) values(7, "A");
insert into tb_turma(idt_serie_turma, turma) values(8, "A");
insert into tb_turma(idt_serie_turma, turma) values(9, "A");

insert into ta_bimestre_turma(cod_ta_bimestre, cod_ta_serie_turma) 
values(1, 6),(1, 7),(1, 8),(1, 9),(1, 1),(1, 2),(1, 3),
(2, 6),(2, 7),(2, 8),(2, 9),(2, 1),(2, 2),(2, 3),
(3, 6),(3, 7),(3, 8),(3, 9),(3, 1),(3, 2),(3, 3),
(4, 6),(4, 7),(4, 8),(4, 9),(4, 1),(4, 2),(4, 3);

