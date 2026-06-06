create database GUVI;

use GUVI;


create table branches(
branch_id int primary key identity,
branch_name varchar(100),
branch_admin_name varchar(100)
);
select*from branches;


create table customer_sales(
sale_id int primary key identity(1,1),
branch_id int,
date DATE,
name varchar(100),
mobile_number varchar(15),
product_name varchar(30),
gross_sales decimal(12,2),
received_amount decimal(12,2),
pending_amount AS (gross_sales-received_amount),
status varchar(10) check(status in('open','close')),
foreign key(branch_id) references branches(branch_id)
);

select * from customer_sales;

create table users(
user_id int primary key identity(1,1),
username varchar(100),
password varchar(255),
branch_id int,
role varchar(20) check(role in('Super Admin','Admin')),
email varchar(255) unique,
foreign key(branch_id) references branches(branch_id)
);

select* from users;

create table payment_splits(
payment_id int primary key identity(10000,1),
sale_id int,
payment_date DATE,
amount_paid decimal(12,2),
payment_method varchar(50)
foreign key(sale_id) references customer_sales(sale_id)
);


select * from payment_splits;

create trigger trg_customer_sales
on payment_splits
after insert
as 
begin;
     update cs
     set cs.received_amount=(
     select sum(ps.amount_paid)
     from payment_splits ps
     where ps.sale_id=cs.sale_id
     ),
     cs.status=case
     when(cs.gross_sales-(
     select sum(ps.amount_paid)
     from payment_splits ps
     where ps.sale_id=cs.sale_id
     )) = 0 then'close'
     else'open'
     end
     from customer_sales cs
     inner join inserted i
     on cs.sale_id=i.sale_id
end;


