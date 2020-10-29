from db import db


class BlackListedJWIModel(db.Model):
    __tablename__ = "black_listed_JWIs"
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(80))

    def __init__(self, jti):
        self.jti = jti

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_blacklisted(cls, jti):
        jti_that_found_in_db = cls.query.filter_by(jti=jti).first()
        if jti_that_found_in_db:
            return True
        return False
