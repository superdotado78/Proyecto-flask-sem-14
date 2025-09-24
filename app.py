from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from repository import (
    init_db, crear_producto, listar_todos, obtener_por_id,
    eliminar_producto, actualizar_nombre, actualizar_cantidad, actualizar_precio,
    buscar_por_nombre,
    crear_usuario, listar_usuarios, obtener_usuario_por_id,
    actualizar_usuario, eliminar_usuario,
    obtener_usuario_por_mail
)
from models import Producto, Usuario

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"

# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Inicializar base de datos
init_db()

# Cargar usuario desde MySQL
@login_manager.user_loader
def load_user(user_id):
    usuario = obtener_usuario_por_id(int(user_id))
    if usuario:
        return Usuario(usuario['idusuario'], usuario['nombre'], usuario['mail'])
    return None

# -------------------- RUTAS PRODUCTOS --------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inventario")
def inventario():
    productos = listar_todos()
    return render_template("inventario.html", productos=productos)

@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        nombre = request.form["nombre"]
        cantidad = int(request.form["cantidad"])
        precio = float(request.form["precio"])
        producto = Producto(None, nombre, cantidad, precio)
        crear_producto(producto)
        flash("Producto agregado correctamente.", "success")
        return redirect(url_for("inventario"))
    return render_template("agregar.html")
    
@app.route("/actualizar/<int:id>", methods=["GET", "POST"])
def actualizar(id):
    if request.method == "POST":
        nombre = request.form["nombre"]
        cantidad = int(request.form["cantidad"])
        precio = float(request.form["precio"])
        actualizar_nombre(id, nombre)
        actualizar_cantidad(id, cantidad)
        actualizar_precio(id, precio)
        flash("Producto actualizado correctamente.", "success")
        return redirect(url_for("inventario"))
    producto = obtener_por_id(id)
    return render_template("actualizar.html", producto=producto)

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    eliminar_producto(id)
    flash("Producto eliminado correctamente.", "success")
    return redirect(url_for("inventario"))
    
# -------------------- RUTAS USUARIOS --------------------

@app.route("/usuarios")
def usuarios():
    usuarios = listar_usuarios()  # Debe retornar [{'id':..., 'nombre':..., 'correo':...}, ...]
    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/crear_usuario", methods=["GET", "POST"])
def crear_usuario_web():
    if request.method == "POST":
        nombre = request.form["nombre"]
        mail = request.form["mail"]
        crear_usuario(nombre, mail)
        flash("Usuario creado correctamente.", "success")
        return redirect(url_for("usuarios"))
    return render_template("crear_usuario.html")

@app.route("/editar_usuario/<int:idusuario>", methods=["GET", "POST"])
def editar_usuario(idusuario):
    usuario = obtener_usuario_por_id(idusuario)
    if not usuario:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for("usuarios"))
    if request.method == "POST":
        nombre = request.form["nombre"]
        mail = request.form["mail"]
        actualizar_usuario(idusuario, nombre, mail)
        flash("Usuario actualizado correctamente.", "success")
        return redirect(url_for("usuarios"))
    return render_template("editar_usuario.html", usuario=usuario)

@app.route("/eliminar_usuario/<int:idusuario>", methods=["POST"])
def eliminar_usuario_web(idusuario):
    eliminar_usuario(idusuario)
    flash("Usuario eliminado correctamente.", "success")
    return redirect(url_for("usuarios"))

# -------------------- RUTAS LOGIN --------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mail = request.form["mail"].strip()
        nombre = request.form["nombre"].strip()
        usuario_db = obtener_usuario_por_mail(mail)
        if usuario_db and usuario_db["nombre"] == nombre:
            user = Usuario(usuario_db["idusuario"], usuario_db["nombre"], usuario_db["mail"])
            login_user(user)
            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for("protegida"))
        else:
            flash("Credenciales inválidas. Por favor, verifica tu nombre y correo.", "danger")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("index"))

@app.route("/protegida")
@login_required
def protegida():
    return render_template("protegida.html")

# -------------------- RUN APP --------------------

if __name__ == "__main__":
    app.run(debug=True)