DROP TABLE IF EXISTS query_builder.public.user;
DROP TABLE IF EXISTS query_builder.public.activation_code;


create table query_builder.public."user" (
  username character varying(50) not null, -- Username
  password character varying(256) not null, -- Hashed user password
  email character varying(256) not null
      constraint user_pk
            unique, -- Email
  created_at timestamp without time zone not null, -- User created at
  updated_at timestamp without time zone, -- User updated at
  is_active boolean not null,
  id bigint primary key not null default nextval('user_id_seq'::regclass)
);
comment on column query_builder.public."user".username is 'Username';
comment on column query_builder.public."user".password is 'Hashed user password';
comment on column query_builder.public."user".email is 'Email';
comment on column query_builder.public."user".created_at is 'User created at';
comment on column query_builder.public."user".updated_at is 'User updated at';

create table query_builder.public.activation_code
(
    id              bigserial
        constraint activation_code_pk
            primary key,
    user_id         bigint       not null
        constraint activation_code_user_id_fk
            references query_builder.public."user",
    activation_code varchar(256) not null,
    is_active       boolean      not null,
    created_at      timestamp    not null,
    updated_at      timestamp
);

comment on table query_builder.public.activation_code is 'Activation code to check an email';

comment on column query_builder.public.activation_code.user_id is 'Foreign key to user table';

alter table query_builder.public.activation_code
    owner to postgres;

