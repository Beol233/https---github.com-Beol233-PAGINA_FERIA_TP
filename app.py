from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def inicio():
    print("Hola")
    return render_template('login.html')

# @app.route("/login", methods=["POST"])
# def login():

#     usuario = request.form["usuario"]
#     password = request.form["password"]

#     print(usuario)
#     print(password)

#     return render_template("libros/libros.html")

# @app.route("/busqueda_libro", methods=["GET"])
# def busqueda_libro():
#     return





if __name__=="__main__":   
    app.run(debug=True)
