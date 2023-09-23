CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    setor VARCHAR(20) NOT NULL,
    funcao VARCHAR(10) DEFAULT 'user',
    negocio ENUM('curtume', 'estofados'),
    email VARCHAR(30) NOT NULL,
    dt_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP);