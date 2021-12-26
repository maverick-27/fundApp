from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class FundModel(db.Model):
    __tablename__ = "table"

    fund_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    source = db.Column(db.String())
    effective_date = db.Column(db.String(80))
    future_effective_date = db.Column(db.String())

    def __init__(self, fund_id, name, source, effective_date, future_effective_date):
        self.fund_id = fund_id
        self.name = name
        self.source = source
        self.effective_date = effective_date
        self.future_effective_date = future_effective_date

    def __repr__(self):
        return f"{self.name}:{self.fund_id}"