import mysql.connector


class SQL:
    def __init__(self, usuario="08ezYU3bp0", senha="owSllN0RD4", host="remotemysql.com", esquema="08ezYU3bp0"):
        self.cnx = mysql.connector.connect(user=usuario, password=senha,
                                           host=host,
                                           database=esquema)
        self.cs = self.cnx.cursor()

    def executar(self, comando, parametros):
        self.cs.execute(comando, parametros)
        self.cnx.commit()
        return True

    def consultar(self, comando, parametros):
        self.cs.execute(comando, parametros)
        return self.cs

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cnx.close()
        self.cs.close()
