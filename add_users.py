from app import app, db
from models import User
import getpass

def create_user_interactive():
    with app.app_context():
        username = input("أدخل اسم المستخدم: ")
        password = getpass.getpass("أدخل كلمة السر: ")
        is_admin_input = input("هل هو admin؟ (y/n): ").lower()
        is_admin = True if is_admin_input == 'y' else False

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print("المستخدم موجود مسبقاً.")
            return

        user = User(username=username, is_admin=is_admin)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"تم إنشاء المستخدم '{username}' بنجاح.")

if __name__ == "__main__":
    create_user_interactive()
