-- Table: demo.place_demo

-- DROP TABLE demo.place_demo;

CREATE TABLE demo.place_demo
(
    oid integer NOT NULL,
    placeid character(256) COLLATE pg_catalog."default",
    placename character(256) COLLATE pg_catalog."default",
    location geometry,
    category character(256) COLLATE pg_catalog."default",
    num_like integer,
    num_tlk integer,
    num_act integer,
    website character(256) COLLATE pg_catalog."default",
    x real,
    y real,
    CONSTRAINT place_demo_pkey PRIMARY KEY (oid)
)