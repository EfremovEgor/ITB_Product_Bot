from models import UnregisteredUser, RegisteredUser
from database import session

to_create = RegisteredUser(telegram_id=1070199744, name="Егор")

# session.add(to_create)
# session.commit()
# for user in session.query(RegisteredUser).all():
#     print(user.name)
