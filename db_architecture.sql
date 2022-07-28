-- ------------------------------------------------------------------------
-- configuraciones iniciales
SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
-- ------------------------------------------------------------------------

--
-- Roles
--

CREATE ROLE "alkemy";
ALTER ROLE "alkemy" WITH SUPERUSER INHERIT CREATEROLE CREATEDB
LOGIN REPLICATION BYPASSRLS
PASSWORD 'toorpass';

--
-- Database creation
--

CREATE DATABASE "alkemydb" WITH TEMPLATE = template0 OWNER = "alkemy";
REVOKE CONNECT,TEMPORARY ON DATABASE "template1" FROM PUBLIC;
GRANT CONNECT ON DATABASE "template1" TO PUBLIC;


\connect "alkemydb"

-- -----------------------------------------------------------------------

--
CREATE TABLE IF NOT EXISTS "public"."data_principal"(
    "index" serial NOT NULL,
    "cod_localidad" INTEGER DEFAULT NULL,
    "id_provincia" INTEGER DEFAULT NULL,
    "id_departamento" INTEGER DEFAULT NULL,
    "categoria" CHARACTER VARYING DEFAULT NULL,
    "provincia" CHARACTER VARYING DEFAULT NULL,
    "localidad" CHARACTER VARYING DEFAULT NULL,
    "nombre" CHARACTER VARYING DEFAULT NULL,
    "domicilio" CHARACTER VARYING DEFAULT NULL,
    "codigo_postal" INTEGER DEFAULT NULL,
    "telefono" CHARACTER VARYING DEFAULT NULL,
    "mail" CHARACTER VARYING DEFAULT NULL,
    "web" CHARACTER VARYING DEFAULT NULL,
    "fecha_in" timestamp with time zone DEFAULT NOW(),
    PRIMARY KEY("index")
);

ALTER TABLE "public"."data_principal" OWNER TO "alkemy";

-- 
-------------------------------------------------------------------------
--
CREATE TABLE IF NOT EXISTS "public"."totales"(
    "index" serial NOT NULL,
    "categoria" CHARACTER VARYING DEFAULT NULL,
    "total" INTEGER DEFAULT NULL,
    "fecha" timestamp with time zone DEFAULT NOW(),
    PRIMARY KEY("index")
);
ALTER TABLE "public"."totales" OWNER TO "alkemy";

CREATE TABLE IF NOT EXISTS "public"."cines"(
    "index" serial NOT NULL,
    "provincia" CHARACTER VARYING DEFAULT NULL,
    "pantallas" INTEGER DEFAULT NULL,
    "butacas" INTEGER DEFAULT NULL,
    "espacios INCAA" CHARACTER VARYING DEFAULT NULL,
    PRIMARY KEY("index")
);

ALTER TABLE "public"."cines" OWNER TO "alkemy";




