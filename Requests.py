from flask import Flask, render_template

app = Flask(__name__)
#route -> url do site
#função -> o que você quer exibir

@app.route("/")
def homepage():
    return "<p>Olá mundo!</p><p>Estou online</p>"

@app.route("/enviados")
def enviado_msg():
    return "<p>Olá, Gustavo!</p><p>Seja bem-vindo!</p>"

# colocar o site no ar
if __name__ == "__main__":
    app.run(debug=True)
