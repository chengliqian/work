from app import db

class NexApiCase(db.Model):
    # nex api用例表
    __tablename__ = 'nex_api_case'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    desc = db.Column(db.String(100))
    url = db.Column(db.String(100))
    request_type = db.Column(db.String(100))
    request_data = db.Column(db.Text)
    expectation = db.Column(db.String(1000))
    category = db.Column(db.Integer)

    def to_json(self):
        case = {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
            'url': self.url,
            'request_type': self.request_type,
            'request_data': self.request_data,
            'expectation': self.expectation,
            'category': self.category
        }

        return case

    def __init__(self, name, desc, url, request_type, request_data, expectation, category):
        # self.id = id
        self.name = name
        self.desc = desc
        self.url = url
        self.request_data = request_data
        self.request_type = request_type
        self.expectation = expectation
        self.category = category

    @staticmethod
    def count():
        count = NexApiCase.query.count()
        return count

    def __repr__(self):
        return '<Case %r>' % self.name