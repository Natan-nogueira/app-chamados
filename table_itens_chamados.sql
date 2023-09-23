create table itens_chamados(id_iten int primary key auto_increment, 
							id_chamado int, 
							data timestamp current_timestamp , 
							user_id int, 
							observacao text not null, 
							setor varchar(20));