from database import db_session
from models import Probas

class Controllers:
    u = Probas('admin1', 'admin@localhost1')
    db_session.add(u)
    db_session.commit()