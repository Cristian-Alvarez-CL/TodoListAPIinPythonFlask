from flask import Flask, render_template, request, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import db, Test

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand) # db init // crea la carpeta migrations
                                          # db migrate // crea o genera las migraciones por cada model o tabla dentro del archivo models.py
                                          # db upgrade // llevar todas las migrations hacia la base de datos
# GET
@app.route('/', methods=['GET']) # GET, POST, PUT, DELETE
def root():
    return render_template('index.html')

@app.route('/test', methods=['GET', 'POST'])
@app.route('/test/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def test(id = None):

    if request.method == 'GET':
        if id is not None:
            tests = Test.query.get(id)
            if not tests: return jsonify({"msg": "Registro no encontrado"}), 404
            return jsonify(tests.serialize()), 200
        else:
            tests = Test.query.all()
            tests = list(map(lambda test: test.serialize(), tests))
            return jsonify(tests), 200

    if request.method == 'POST':
        label = request.json.get('label')
        done = request.json.get('done')
        if not label: return jsonify({"msg": "name is required"}), 400
        if not done: return jsonify({"msg": "name is required"}), 400
        test = Test()
        test.label = label
        test.done = done
        test.save()
        return jsonify(test.serialize()), 201
        
    if request.method == 'PUT':
        label = request.json.get('label')
        done = request.json.get('done')
        
        tests = Test.query.get(id)
        if not tests: return jsonify({"msg": "Registro no encontrado"}), 404

        tests.label = label
        tests.done = done

        tests.update()

        return jsonify(tests.serialize()), 201

    if request.method == 'DELETE':
        tests = Test.query.get(id)
        if not tests: return jsonify({"msg": "Contact not found"}), 404
        tests.delete()
        return jsonify({"msg": "Registro Borrado"}), 200

if __name__ == '__main__':
    manager.run()