CREATE TABLE IF NOT EXISTS commands (
    command VARCHAR(20) PRIMARY KEY,
    server_url VARCHAR(200)
);

insert into commands(command,server_url) values 
('shrug','http://shrug_command:5051'),
('email','http://email_command:5052'); 