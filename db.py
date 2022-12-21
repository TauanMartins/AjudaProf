import mysql.connector


class SQL:
    def __init__(self, usuario="root", senha="", host="127.0.0.1", esquema="Ajuda_Prof"):
        # conexao anterior  usuario="08ezYU3bp0", senha="owSllN0RD4", host="remotemysql.com", esquema="08ezYU3bp0"
        self.cnx = mysql.connector.connect(user=usuario, password=senha,
                                           host=host,
                                           database=esquema)
        self.cs = self.cnx.cursor(buffered=True)

    def executar(self, comando, parametros):
        self.cs.execute(comando, parametros)
        return True

    def consultar(self, comando, parametros):
        self.cs.execute(comando, parametros)
        return self.cs

    def __del__(self):
        self.cnx.close()
        self.cs.close()
