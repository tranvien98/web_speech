from flask_mongoengine import MongoEngine


db = MongoEngine()
class FileAudio(db.Document):
    id_audio = db.StringField(required=True, unique=True)
    filename = db.StringField(required=True)
    create_at = db.StringField(required=True)
    timestamp = db.StringField(required=True)
    path_file = db.StringField(required=True)
    lyrics = db.ListField()
    duration = db.StringField()
    spell_mistake = db.ListField()