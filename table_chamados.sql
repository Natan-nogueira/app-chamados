create table chamados(id int auto_increment, primary key,
                      titulo varchar(50) not null,
                      descricao text not null,
                      data_abertura timestamp default current_timestamp,
                      solucao text not null,
                      prioridade varchar(20) not null,
                      categoria varchar(20), not null
                      status varchar(20) default 'Aberto');