DROP TABLE IF EXISTS jersey_sales;
DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    orderid        SERIAL PRIMARY KEY,
    customername   VARCHAR(80) NOT NULL,
    customeremail  VARCHAR(120) NOT NULL,
    orderdate      DATE NOT NULL,
    shippingaddress VARCHAR(120) NOT NULL,
    shippingcity   VARCHAR(60) NOT NULL,
    shippingstate  VARCHAR(20) NOT NULL,
    shippingzip    VARCHAR(10) NOT NULL,
    paymentmethod  VARCHAR(20) NOT NULL,
    ordertotal     NUMERIC(10,2) NOT NULL
);

CREATE TABLE jersey_sales (
    jerseyid       SERIAL PRIMARY KEY,
    orderid        INT NOT NULL REFERENCES orders(orderid),
    jerseyname     VARCHAR(80) NOT NULL,
    jerseynumber   INT NOT NULL,
    team           VARCHAR(50) NOT NULL,
    jerseytype     VARCHAR(15) NOT NULL,
    jerseyyear     INT NOT NULL,
    jerseysize     VARCHAR(5) NOT NULL,
    jerseyprice    NUMERIC(8,2) NOT NULL,
    quantitysold   INT NOT NULL,
    datesold       DATE NOT NULL
);

