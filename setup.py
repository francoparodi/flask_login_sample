from flask_login_sample import db
print('Creating db...')
db.create_all()
from flask_login_sample.models import User 
u = User(username="admin", email="admin@localhost.com", role="ADMIN", enabled=1)
u.set_password_hash("adminadmin")
db.session.add(u)
u = User(username="user", email="user@localhost.com",  role="USER", enabled=1)
u.set_password_hash("useruser")
db.session.add(u)
db.session.commit()
print('Installation completed.')
exit()