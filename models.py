from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable=False)
    done = db.Column(db.String(100), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "label": self.label,
            "done": self.done
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()