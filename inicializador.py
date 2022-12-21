from checar_sessao import *
from ajuda_prof import AjudaProf


class Iniciar:
    def __init__(self):
        app = Flask(__name__)
        app.secret_key = "SenhaSecreta"
        app.permanent_session_lifetime = timedelta(minutes=60)
        AjudaProf(app)
        if __name__ == '__main__':
            app.run(debug=True)


Iniciar()
