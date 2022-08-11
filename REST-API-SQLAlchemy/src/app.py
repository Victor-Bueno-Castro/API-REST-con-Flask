from flask import Flask, request, jsonify #   Módulo para trabajar con flask
from flask_sqlalchemy import SQLAlchemy #   Módulo para trabajar con las bases de datos SQLAlchemy
from flask_marshmallow import Marshmallow   #   Módulo para definir el esquema

app = Flask(__name__)   #   Instancia del módulo Flask

#   Instancia para el módulo de SQLAlchemy con la dirección de la Base de Datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#   Instanciar la BD para el ORM
db = SQLAlchemy(app)
ma = Marshmallow(app)   #   Instancia de marshmallow

#   En esta clase se define el ORM para la BD
class Task(db.Model):
    
    #   Creación de la tabla
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))
    
    #   Instanciar la clase y definirla
    def __init__(self, title, description):
        self.title = title
        self.description = description

#   Crear la tabla
db.create_all()

#   Creación del esquema para interacturar con la BD
class TaskSchema(ma.Schema):
    class Meta:
        #   Se definen los campos para interacturar con el esquema
        fields = ['id', 'title', 'description']
        
#   Instanciar el esquema
task_schema = TaskSchema() 
tasks_schema = TaskSchema(many=True) #   Permite obtener múltiples respuestas 

#   Definición de los endpoints
#   Método POST para crear las tareas
@app.route('/tasks', methods=['POST'])
#   Función para crear una tarea
def create_task():
    
    #   Recibe los datos que envía el cliente
    title = request.json['title']
    description = request.json['description']
    
    new_task = Task(title, description) #   Se crea la nueva tarea
    db.session.add(new_task)    #   Se agrega la nueva tarea a la BD
    db.session.commit() #   Se guardan los cambios
    
    return task_schema.jsonify(new_task)    #   Retorna la tarea en formato JSON

#   Definición de una segunda ruta para obtener todas las tareas (GET)
@app.route('/tasks', methods=['GET'])
def get_tasks():
    
    #   Consultar todo
    all_tasks = Task.query.all()    #   Devuelve todas las tareas
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)  #   Convierte el objeto Python a JSON

#   Verificar una tarea mediante su ID
@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    
    task = Task.query.get(id)
    return task_schema.jsonify(task)

#   Actualizar una tarea filtrando por su id (PUT)
@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    
   task = Task.query.get(id)
   
   #    Datos para actualizar
   title = request.json['title']
   description = request.json['description']
   
   task.title = title
   task.description = description
   
   db.session.commit()
   return task_schema.jsonify(task)

#   Eliminar una tarea filtrando su id (DELETE)
@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return task_schema.jsonify(task)

#   Iniciar app
if __name__ == '__main__':
    app.run(debug=True)