-- Database: messangerdb

DROP DATABASE IF EXISTS messangerdb;
CREATE DATABASE messangerdb
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Table: cities

DROP TABLE IF EXISTS public.cities;
CREATE TABLE IF NOT EXISTS public.cities
(
    city character varying(128) COLLATE pg_catalog."default" NOT NULL,
    domain character varying(128) COLLATE pg_catalog."default" NOT NULL,
    population integer
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.cities OWNER to postgres;

-- Table: main_messages

DROP TABLE IF EXISTS public.main_messages;
CREATE TABLE IF NOT EXISTS public.main_messages
(
    telegram_id integer NOT NULL,
    message_id integer NOT NULL,
    CONSTRAINT main_messages_telegram_id_key UNIQUE (telegram_id)
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.main_messages OWNER to postgres;

-- Table: photos

DROP TABLE IF EXISTS public.photos;
CREATE TABLE IF NOT EXISTS public.photos
(
    telegram_id integer NOT NULL,
    photo_id text COLLATE pg_catalog."default" NOT NULL
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.photos OWNER to postgres;

-- Table: states

DROP TABLE IF EXISTS public.states;
CREATE TABLE IF NOT EXISTS public.states
(
    telegram_id integer NOT NULL,
    recording boolean NOT NULL,
    recording_type character varying(3) COLLATE pg_catalog."default",
    recording_stage character varying(3) COLLATE pg_catalog."default",
    on_chatting boolean NOT NULL,
    CONSTRAINT states_pkey PRIMARY KEY (telegram_id)
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.states OWNER to postgres;

-- Table: users

DROP TABLE IF EXISTS public.users;
CREATE TABLE IF NOT EXISTS public.users
(
    telegram_id integer NOT NULL,
    first_name character varying(128) COLLATE pg_catalog."default" NOT NULL,
    last_name character varying(128) COLLATE pg_catalog."default" NOT NULL,
    telegram_name character varying(128) COLLATE pg_catalog."default" NOT NULL,
    registration_date timestamp without time zone NOT NULL,
    language character(2) COLLATE pg_catalog."default"
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users OWNER to postgres;

-- Table: users_info

DROP TABLE IF EXISTS public.users_info;
CREATE TABLE IF NOT EXISTS public.users_info
(
    telegram_id integer NOT NULL,
    age smallint,
    age_wish int4range,
    city character varying(32) COLLATE pg_catalog."default",
    city_wish character varying(32) COLLATE pg_catalog."default",
    sex boolean,
    sex_wish boolean,
    description character(350) COLLATE pg_catalog."default",
    interlocutor_id integer,
    CONSTRAINT info_users_pkey PRIMARY KEY (telegram_id)
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users_info OWNER to postgres;

-- Table: users_searching_buffer

DROP TABLE IF EXISTS public.users_searching_buffer;
CREATE TABLE IF NOT EXISTS public.users_searching_buffer
(
    telegram_id integer NOT NULL,
    buffering_time time without time zone NOT NULL,
    specified boolean NOT NULL,
    CONSTRAINT users_searching_buffer_pkey PRIMARY KEY (telegram_id)
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users_searching_buffer OWNER to postgres;
