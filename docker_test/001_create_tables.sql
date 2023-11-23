/**
*   Создание таблиц
*/

CREATE TABLE public.fact_revenue (
	id serial4 PRIMARY KEY,
	sk_account_id int4 NOT NULL,
	sk_cfo_id int4 NOT NULL,
	value int8 NOT NULL
);

CREATE TABLE public.dim_account (
	sk_account_id int4 NOT NULL,
	bk_account_id varchar(20) NOT NULL,
	bk_account_name varchar(28) NOT NULL,
	bk_combined_map varchar(20) NOT NULL
);

CREATE TABLE public.dim_cfo (
	sk_cfo_id int4 NOT NULL,
	bk_cfo_id varchar(20) NOT NULL,
	bk_cfo_name varchar(20) NOT NULL
);

CREATE TABLE public.fact_sold (
	id serial4 PRIMARY KEY,
	sk_item_id int4 NOT NULL,
	sk_cfo_id int4 NOT NULL,
	value int8 NOT NULL
);

CREATE TABLE public.dim_item (
	sk_item_id int4 NOT NULL,
	bk_item_id varchar(20) NOT NULL,
	bk_item_name varchar(20) NOT NULL,
	bk_combined_map varchar(20) NOT NULL
);

