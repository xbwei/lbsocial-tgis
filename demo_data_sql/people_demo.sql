-- Table: demo.people_demo

-- DROP TABLE demo.people_demo;

CREATE TABLE demo.people_demo
(
    username character(256) COLLATE pg_catalog."default",
    userid character(256) COLLATE pg_catalog."default",
    url character(2048) COLLATE pg_catalog."default",
    fromusername character(256) COLLATE pg_catalog."default",
    fromuserid character(256) COLLATE pg_catalog."default",
    loccount integer,
    oid integer NOT NULL,
    CONSTRAINT people_demo_pkey PRIMARY KEY (oid)
)
