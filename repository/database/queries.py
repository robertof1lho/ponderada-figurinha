class BaseQuery:
    def __init__(self, params: dict = None):
        self.params = params or {}


class Select(BaseQuery):
    ALL                 = "SELECT * FROM figurinhas"
    BY_ID               = "SELECT * FROM figurinhas WHERE id = :id"
    BY_POSICAO          = "SELECT * FROM figurinhas WHERE posicao = :posicao"
    BY_TIPO             = "SELECT * FROM figurinhas WHERE tipo = :tipo"
    BY_POSICAO_AND_TIPO = "SELECT * FROM figurinhas WHERE posicao = :posicao AND tipo = :tipo"


class Insert(BaseQuery):
    FIGURINHA = """
        INSERT INTO figurinhas (numero, nome, selecao, tipo, posicao, created_at, updated_at)
        VALUES (:numero, :nome, :selecao, :tipo, :posicao, :created_at, :updated_at)
    """


class Update(BaseQuery):
    FIGURINHA = """
        UPDATE figurinhas
        SET numero = :numero, nome = :nome, selecao = :selecao,
            tipo = :tipo, posicao = :posicao, updated_at = :updated_at
        WHERE id = :id
    """


class Delete(BaseQuery):
    FIGURINHA = "DELETE FROM figurinhas WHERE id = :id"
