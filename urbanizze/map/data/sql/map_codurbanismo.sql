--
-- PostgreSQL database dump
--

-- Dumped from database version 10.2
-- Dumped by pg_dump version 10.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: map_codurbanismo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE map_codurbanismo (
    id integer NOT NULL,
    zona character varying(50) NOT NULL,
    uso_permitido character varying(50) NOT NULL,
    area_minima character varying(50) NOT NULL,
    frente_minima character varying(50) NOT NULL,
    taxa_ocupacao character varying(50) NOT NULL,
    altura_maxima character varying(50) NOT NULL,
    afast_frente character varying(50) NOT NULL,
    afast_lateral character varying(50) NOT NULL,
    afast_fundos character varying(50) NOT NULL
);


ALTER TABLE map_codurbanismo OWNER TO postgres;

--
-- Name: map_codurbanismo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE map_codurbanismo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE map_codurbanismo_id_seq OWNER TO postgres;

--
-- Name: map_codurbanismo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE map_codurbanismo_id_seq OWNED BY map_codurbanismo.id;


--
-- Name: map_codurbanismo id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY map_codurbanismo ALTER COLUMN id SET DEFAULT nextval('map_codurbanismo_id_seq'::regclass);


--
-- Data for Name: map_codurbanismo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY map_codurbanismo (id, zona, uso_permitido, area_minima, frente_minima, taxa_ocupacao, altura_maxima, afast_frente, afast_lateral, afast_fundos) FROM stdin;
1	ZA-3	Residencial 5	600	20	30	4	5	4	4
2	ZA-3	Residencial 5 (1)	600	20	40	Pilotis + 4 pv + Cobertura	5	4	4
3	ZA-3	Residencial 6	600	30	30	-	5	4+(h/10)	4+(h/10)
4	ZT-2	Comércio local (CL) ou Serviço Local (SL)	360	12	50	2	5	1.5	3
5	ZT-2	Comércio de Bairro (CB) ou Serviço de Bairro (SB)	450	15	50	3	5	2.0	3
6	ZT-2	Serviço de Bairro (Flat)	360	12	TE=70 DE=50	4	5	TE=0,0 DE=2,00	3
7	ZT-2	Comércio Principal (CP) ou Serviço Principal (SP)	600	20	TE=70 1° ao 3° = 50 DE=50	-	5	TE=0,0 1° ao 3° = 2,0 DE= 4+(h/10)	Até o 4° = 3,0 DE= 4+(h/10)
8	ZT-2	Serviço Principal (Flat)	600	15	TE=70 1° ao 3° = 50 DE=50	>=5	5	TE=0,0 1° ao 3° = 2,0 DE= 4+(h/10)	Até o 4° = 3,0 DE= 4+(h/10)
9	ZR-1	Residencial 5	600	15	40	Pilotis + 4 pv + Cobertura	5	4	4
10	ZR-1	Residencial 5 (2)	600	15	35	4	5	4	4
11	ZR-1	Residencial 6	900	30	30	-	5	4+(h/10)	4+(h/10)
14	ZA-3	Comércio Principal (CP) ou Serviço Principal (SP)	600	20	TE+2 =70 DE =40	-	5	TE=0.0 AT... 2°= 2.00 DE =3+(h/10)	AT... 3°=2.0 DE=3+(h/10)
\.


--
-- Name: map_codurbanismo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('map_codurbanismo_id_seq', 14, true);


--
-- Name: map_codurbanismo map_codurbanismo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY map_codurbanismo
    ADD CONSTRAINT map_codurbanismo_pkey PRIMARY KEY (id);


--
-- Name: TABLE map_codurbanismo; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE map_codurbanismo TO urbanizze;


--
-- PostgreSQL database dump complete
--

