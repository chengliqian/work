from datetime import datetime
from app import db

class ServerMonitor(db.Model):
    __tablename__ = 'server_monitor'
    id = db.Column(db.Integer, primary_key=True)
    cpu_info = db.Column(db.String(1000))
    disks_info = db.Column(db.String(1000))
    memory_info = db.Column(db.String(1000))
    network_info = db.Column(db.String(1000))
    sensors_info = db.Column(db.String(1000))
    moniter_time = db.Column(db.DateTime, default=datetime.utcnow)