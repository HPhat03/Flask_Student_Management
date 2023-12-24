import enum

from Project import app, db
from sqlalchemy import Column, Integer,String,Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import  relationship
from flask_login import UserMixin
class UserRole(enum.Enum):
    NHANVIEN = 1,
    GIAOVIEN = 2,
    ADMIN = 3
class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key= True, autoincrement= True, nullable= False)
    created_date = Column(DateTime)
    active = Column(Boolean, default= True)

class User(BaseModel, UserMixin):
    name = Column(String(50), nullable= False)
    username = Column(String(20), nullable= False)
    password = Column(String(100), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.NHANVIEN)
    nhanvien = relationship('NhanVien', backref="info", lazy= True)

class NhanVien(db.Model):
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True,nullable= False)
    started_date = Column(DateTime, nullable=True)

class Admin(BaseModel):
    pass

class GiaoVien(BaseModel):
    pass

if __name__ == "__main__":
    from Project import  app
    with app.app_context():
        db.create_all()

        import hashlib
        u1 = User(name = "Mai Hoàng Phát", username = "mhphat",
                   password = hashlib.md5('123456'.encode("utf-8")).hexdigest(),
                   user_role = UserRole.NHANVIEN)
        # db.session.add(u1)
        # db.session.commit()

        nv1 = NhanVien(info = u1, user_id = 1)