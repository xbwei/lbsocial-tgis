-- Table: demo.activity_demo

-- DROP TABLE demo.activity_demo;

CREATE TABLE demo.activity_demo
(
    fromuserid character(256) COLLATE pg_catalog."default",
    fromusername character(256) COLLATE pg_catalog."default",
    activityid character(256) COLLATE pg_catalog."default",
    location geometry,
    placeid character(256) COLLATE pg_catalog."default",
    placename character(256) COLLATE pg_catalog."default",
    "time" character(256) COLLATE pg_catalog."default",
    username character(256) COLLATE pg_catalog."default",
    userid character(256) COLLATE pg_catalog."default",
    participant json,
    oid integer NOT NULL,
    type character(256) COLLATE pg_catalog."default",
    x real,
    y real,
    z real,
    CONSTRAINT activity_demo_pkey PRIMARY KEY (oid)
)
