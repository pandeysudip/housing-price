def create_classes(db):
    class Pred(db.Model):
        __tablename__ = 'pets'

        id = db.Column(db.Integer, primary_key=True)
        City = db.Column(db.String(64))
        ActualHouseValue = db.Column(db.Float)
        RandomForestPredictedHouseValue = db.Column(db.Float)
        lat = db.Column(db.Float)
        lon = db.Column(db.Float)

        def __repr__(self):
            return '<Pet %r>' % (self.name)
    return Pred
