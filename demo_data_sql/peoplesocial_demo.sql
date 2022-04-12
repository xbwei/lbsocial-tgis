-- Table: demo.peoplesocial_demo

-- DROP TABLE demo.peoplesocial_demo;

CREATE TABLE demo.peoplesocial_demo
(
    oid integer NOT NULL,
    peopleid character(256) COLLATE pg_catalog."default",
    peoplename character(256) COLLATE pg_catalog."default",
    num_node integer,
    num_act integer,
    num_clique integer,
    num_visit integer,
    density real,
    sum_dis real,
    triangles real,
    avg_clu real,
    trans real,
    CONSTRAINT peoplesocial_demo_pkey PRIMARY KEY (oid)
)