create database bank_karmant;

use bank_karmant;

CREATE TABLE CLIENTE(
ID_CLIENTE VARCHAR(20) PRIMARY KEY, 
NOMBRE VARCHAR(100),
APELLIDO_PATERNO VARCHAR(100),
APELLIDO_MATERNO VARCHAR(100),
DIRECCION VARCHAR(200),
FECHA_NACIMIENTO DATE,
TELEFONO VARCHAR(20), 
CORREO VARCHAR(50),
PASSWORD VARCHAR(50)
);

CREATE TABLE TIPO_CUENTA(
ID_TIPO_CUENTA VARCHAR(20) PRIMARY KEY, 
TIPO_CUENTA VARCHAR(100)
);

CREATE TABLE CUENTA(
NUMERO_CUENTA VARCHAR(20) PRIMARY KEY,
ID_CLIENTE VARCHAR(20),
ID_TIPO_CUENTA VARCHAR(20),
SALDO DECIMAL (10,2), 
FECHA_EMISION DATE,
FECHA_VENCIMIENTO DATE,
FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE (ID_CLIENTE),
FOREIGN KEY (ID_TIPO_CUENTA) REFERENCES TIPO_CUENTA (ID_TIPO_CUENTA)
);


CREATE TABLE REGISTRO_DEPOSITO (
    ID_CLIENTE_DEPOSITO VARCHAR(20),
    FECHA_DEPOSITO DATETIME,
    MONTO_DEPOSITO DECIMAL(10,2)
    );


CREATE TABLE registro_transferencia (
    id_cliente_tranfiere VARCHAR(20),
    id_cliente_recibe VARCHAR(20),
    fecha_hora_transferencia DATETIME,
    monto_de_tranferencia decimal(10,2)
    );

CREATE TABLE registro_retiro (
    id_cliente_retira VARCHAR(20),
    fecha_hora_retiro DATETIME,
    monto_de_retiro decimal(10,2)
    );



