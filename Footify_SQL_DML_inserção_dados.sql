-- INSERÇÃO DE DADOS FICT�?CIOS NO FOOTIFY - COM INTEGRIDADE GARANTIDA

UPDATE FO_PRECO_PRODUTO
SET PRECO_LISTADO = PRECO_PROMOCIONAL
WHERE PRECO_LISTADO = 0;

-- Inserir loja 'Nike Oficial' com ID 1 (assumido como sequencial ou gerado por IDENTITY)
DECLARE
    v_id_loja NUMBER;
BEGIN
    SELECT ID_LOJA INTO v_id_loja FROM FO_LOJA WHERE NOME = 'Nike Oficial';
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        INSERT INTO FO_LOJA (NOME, URL_SITE)
        VALUES ('Nike Oficial', 'https://www.nike.com.br')
        RETURNING ID_LOJA INTO v_id_loja;
END;
/

-- Produto 1
DECLARE
    v_id_produto NUMBER;
    v_id_loja NUMBER;
BEGIN
    SELECT ID_LOJA INTO v_id_loja FROM FO_LOJA WHERE NOME = 'Nike Oficial';

    INSERT INTO FO_PRODUTO (NOME, DESCRICAO, MARCA, CATEGORIA, URL_IMAGEM)
    VALUES ('Nike Air Force 1 ''07 Essential', 'Let your shoe game shimmer in the Nike Air Force 1 ''07 Essential.', 'Nike', 'Corrida', 'https://static.nike.com/a/images/t_PDP_1728_...jpg')
    RETURNING ID_PRODUTO INTO v_id_produto;

    INSERT INTO FO_CARACTERISTICA_PRODUTO (ID_PRODUTO, TIPO_USO, GENERO_DESTINADO, COR_PREDOMINANTE, TAMANHO_DISPONIVEL)
    VALUES (v_id_produto, 'corrida', 'unissex', 'preto', '42');

    INSERT INTO FO_PRECO_PRODUTO (ID_PRODUTO, ID_LOJA, PRECO_LISTADO, PRECO_PROMOCIONAL, URL_PAGINA_PRODUTO)
    VALUES (v_id_produto, v_id_loja, 0.0, 7495.0, 'https://www.nike.com.br/produto-1');
END;
/

-- Produto 2
DECLARE
    v_id_produto NUMBER;
    v_id_loja NUMBER;
BEGIN
    SELECT ID_LOJA INTO v_id_loja FROM FO_LOJA WHERE NOME = 'Nike Oficial';

    INSERT INTO FO_PRODUTO (NOME, DESCRICAO, MARCA, CATEGORIA, URL_IMAGEM)
    VALUES ('Nike Air Force 1 ''07', 'The legend lives on in the Nike Air Force 1 ''07.', 'Nike', 'Corrida', 'https://static.nike.com/a/images/t_PDP_1728_...jpg')
    RETURNING ID_PRODUTO INTO v_id_produto;

    INSERT INTO FO_CARACTERISTICA_PRODUTO (ID_PRODUTO, TIPO_USO, GENERO_DESTINADO, COR_PREDOMINANTE, TAMANHO_DISPONIVEL)
    VALUES (v_id_produto, 'corrida', 'unissex', 'preto', '42');

    INSERT INTO FO_PRECO_PRODUTO (ID_PRODUTO, ID_LOJA, PRECO_LISTADO, PRECO_PROMOCIONAL, URL_PAGINA_PRODUTO)
    VALUES (v_id_produto, v_id_loja, 0.0, 7495.0, 'https://www.nike.com.br/produto-2');
END;
/

-- Produto 3
DECLARE
    v_id_produto NUMBER;
    v_id_loja NUMBER;
BEGIN
    SELECT ID_LOJA INTO v_id_loja FROM FO_LOJA WHERE NOME = 'Nike Oficial';

    INSERT INTO FO_PRODUTO (NOME, DESCRICAO, MARCA, CATEGORIA, URL_IMAGEM)
    VALUES ('Nike Air Force 1 Sage Low LX', 'Taking both height and craft to new levels, the Nike Air Force 1 Sage Low LX reimagines hoops style.', 'Nike', 'Corrida', 'https://static.nike.com/a/images/t_PDP_1728_...jpg')
    RETURNING ID_PRODUTO INTO v_id_produto;

    INSERT INTO FO_CARACTERISTICA_PRODUTO (ID_PRODUTO, TIPO_USO, GENERO_DESTINADO, COR_PREDOMINANTE, TAMANHO_DISPONIVEL)
    VALUES (v_id_produto, 'corrida', 'unissex', 'preto', '42');

    INSERT INTO FO_PRECO_PRODUTO (ID_PRODUTO, ID_LOJA, PRECO_LISTADO, PRECO_PROMOCIONAL, URL_PAGINA_PRODUTO)
    VALUES (v_id_produto, v_id_loja, 0.0, 9995.0, 'https://www.nike.com.br/produto-3');
END;
/

-- Produto 4
DECLARE
    v_id_produto NUMBER;
    v_id_loja NUMBER;
BEGIN
    SELECT ID_LOJA INTO v_id_loja FROM FO_LOJA WHERE NOME = 'Nike Oficial';

    INSERT INTO FO_PRODUTO (NOME, DESCRICAO, MARCA, CATEGORIA, URL_IMAGEM)
    VALUES ('Nike Air Max Dia SE', 'Designed for a woman''s foot, the Nike Air Max Dia SE delivers a lifted look with an airy aesthetic.', 'Nike', 'Corrida', 'https://static.nike.com/a/images/t_PDP_1728_...jpg')
    RETURNING ID_PRODUTO INTO v_id_produto;

    INSERT INTO FO_CARACTERISTICA_PRODUTO (ID_PRODUTO, TIPO_USO, GENERO_DESTINADO, COR_PREDOMINANTE, TAMANHO_DISPONIVEL)
    VALUES (v_id_produto, 'corrida', 'unissex', 'preto', '42');

    INSERT INTO FO_PRECO_PRODUTO (ID_PRODUTO, ID_LOJA, PRECO_LISTADO, PRECO_PROMOCIONAL, URL_PAGINA_PRODUTO)
    VALUES (v_id_produto, v_id_loja, 0.0, 9995.0, 'https://www.nike.com.br/produto-4');
END;
/

-- Produto 5
DECLARE
    v_id_produto NUMBER;
    v_id_loja NUMBER;
BEGIN
    SELECT ID_LOJA INTO v_id_loja FROM FO_LOJA WHERE NOME = 'Nike Oficial';

    INSERT INTO FO_PRODUTO (NOME, DESCRICAO, MARCA, CATEGORIA, URL_IMAGEM)
    VALUES ('Nike Air Max Verona', 'Pass on the good vibes in the Nike Air Max Verona.', 'Nike', 'Corrida', 'https://static.nike.com/a/images/t_PDP_1728_...jpg')
    RETURNING ID_PRODUTO INTO v_id_produto;

    INSERT INTO FO_CARACTERISTICA_PRODUTO (ID_PRODUTO, TIPO_USO, GENERO_DESTINADO, COR_PREDOMINANTE, TAMANHO_DISPONIVEL)
    VALUES (v_id_produto, 'corrida', 'unissex', 'preto', '42');

    INSERT INTO FO_PRECO_PRODUTO (ID_PRODUTO, ID_LOJA, PRECO_LISTADO, PRECO_PROMOCIONAL, URL_PAGINA_PRODUTO)
    VALUES (v_id_produto, v_id_loja, 0.0, 9995.0, 'https://www.nike.com.br/produto-5');
END;
/
