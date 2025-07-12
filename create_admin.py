from app import app, db
from models import User

with app.app_context():
    # إنشاء المستخدم admin
    admin = User(username="admin", is_admin=True)
    admin.set_password("SGTMSAFI25")  # بدّلها بكلمة السر لي بغيت
    db.session.add(admin)
    db.session.commit()
    print("Admin user created successfully.")
