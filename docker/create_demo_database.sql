create user vector_user;
set password for vector_user = password('s3cret');
grant all on *.* to vector_user;

drop database if exists vector_demo;
create database vector_demo;
use vector_demo;

create table articles (id int PRIMARY KEY AUTO_INCREMENT, document longtext,
                       embedding blob not null
                       /*, vector index (embedding) */) charset=utf8 engine=MyISAM;
