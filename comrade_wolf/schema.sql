DROP TABLE IF EXISTS query_builder.public.user;

CREATE TABLE query_builder.public.user (
  id bigserial PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);
