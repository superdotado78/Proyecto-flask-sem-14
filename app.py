# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from repository import (
    init_db, crear_producto, eliminar_producto,
    actualizar_cantidad, actualizar_precio, actualizar_nombre,
    buscar_por_nombre, listar_todos, obtener_por_id
)
from models import Producto

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"  # Necesaria para flash messages

# Inicializa la base de datos al arrancar
init_db()

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
        try:
            id_ = int(request.form["id"])
            nombre = request.form["nombre"]
            cantidad = int(request.form["cantidad"])
            precio = float(request.form["precio"])
            producto = Producto(id_, nombre, cantidad, precio)
            crear_producto(producto)
            flash("Producto agregado exitosamente.", "success")
            return redirect(url_for("inventario"))
        except Exception as e:
            flash(str(e), "danger")
    return render_template("agregar.html")

@app.route("/eliminar/<int:id_>")
def eliminar(id_):
    try:
        eliminar_producto(id_)
        flash(f"Producto con ID {id_} eliminado.", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("inventario"))

@app.route("/actualizar/<int:id_>", methods=["GET", "POST"])
def actualizar(id_):
    producto = obtener_por_id(id_)
    if not producto:
        flash("Producto no encontrado.", "danger")
        return redirect(url_for("inventario"))

    if request.method == "POST":
        try:
            nuevo_nombre = request.form["nombre"]
            nueva_cantidad = int(request.form["cantidad"])
            nuevo_precio = float(request.form["precio"])
            actualizar_nombre(id_, nuevo_nombre)
            actualizar_cantidad(id_, nueva_cantidad)
            actualizar_precio(id_, nuevo_precio)
            flash("Producto actualizado correctamente.", "success")
            return redirect(url_for("inventario"))
        except Exception as e:
            flash(str(e), "danger")

    return render_template("actualizar.html", producto=producto)

@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    resultados = []
    if request.method == "POST":
        patron = request.form["patron"]
        resultados = buscar_por_nombre(patron)
    return render_template("buscar.html", resultados=resultados)

if __name__ == "__main__":
    app.run(debug=True)
