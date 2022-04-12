-- Table: demo.placesocial_demo

-- DROP TABLE demo.placesocial_demo;

CREATE TABLE demo.placesocial_demo
(
    oid integer NOT NULL,
    placeid character(256) COLLATE pg_catalog."default",
    placename character(256) COLLATE pg_catalog."default",
    num_node integer,
    num_act integer,
    num_clique integer,
    num_visit integer,
    density real,
    triangles real,
    trans real,
    avg_clu real,
    CONSTRAINT placesocial_demo_pkey PRIMARY KEY (oid)
)