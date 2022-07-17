from flask import Flask ,jsonify,request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)
CORS(app)
# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://sql10506996:Ni9MKKTCeL@sql10.freesqldatabase.com/sql10506996'
#                                               user:clave@localhost/nombreBaseDatos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db= SQLAlchemy(app)
ma=Marshmallow(app)
# defino la tabla
class Producto(db.Model):   # la clase Producto hereda de db.Model     
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    nombre=db.Column(db.String(1000))
    precio=db.Column(db.Integer)
    stock=db.Column(db.Integer)
    foto=db.Column(db.String(1000))




    def __init__(self,nombre,precio,stock,foto):   #crea el  constructor de la clase
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.precio=precio
        self.stock=stock
        self.foto=foto


db.create_all()  # crea las tablas
#  ************************************************************
class ProductoSchema(ma.Schema):
    class Meta: #machea los campos con los valores para generar el JSON
        fields=('id','nombre','precio','stock','foto')
producto_schema=ProductoSchema()            # para crear un producto
productos_schema=ProductoSchema(many=True)  # multiples registros

# programo los mapeos, o las rutas, o los endpoints, la URL
@app.route('/index2.html')


@app.route('/productos',methods=['GET'])
def get_Productos():
    all_productos=Producto.query.all()     # query.all() lo hereda de db.Model
    result=productos_schema.dump(all_productos)  # .dump() lo hereda de ma.schema
    return jsonify(result) # retorna un json con todos los productos

@app.route('/productos/<id>',methods=['GET'])
def get_producto(id):
    producto=Producto.query.get(id)
    return producto_schema.jsonify(producto)

@app.route('/producto/<id>',methods=['DELETE'])
def delete_producto(id):
    producto=Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return producto_schema.jsonify(producto)


@app.route('/productos', methods=['POST']) # endpoint para insertar ruta/(agregar)
def create_producto():
    print(request.json) # request.json contiene el json que envio el cliente
    nombre=request.json['nombre']
    precio=request.json['precio']
    stock=request.json['stock']
    foto=request.json['foto']




    new_producto=Producto(nombre,precio,stock,foto)
    db.session.add(new_producto)
    db.session.commit()
    return producto_schema.jsonify(new_producto)

@app.route('/productos/<id>' ,methods=['PUT']) #(modificar)
def update_producto(id):
    producto=Producto.query.get(id)
    nombre=request.json['nombre']
    precio=request.json['precio']
    stock=request.json['stock']
    foto=request.json['foto']



    producto.nombre=nombre
    producto.precio=precio
    producto.stock=stock
    producto.foto=foto

    db.session.commit()
    return producto_schema.jsonify(producto)
 
# programa principal
if __name__=='__main__':  
    app.run(debug=True, port=5000)  

