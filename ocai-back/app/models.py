from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, Boolean, ForeignKey
from database import Base

class Verification_Token(Base):
  __tablename__ = "verification_token"

  identifier = Column(String, primary_key=True, nullable=True)
  expires = Column(DateTime, nullable=True)
  token = Column(String, nullable=True)

class Accounts(Base):
  __tablename__ = "accounts"

  id = Column(Integer, primary_key=True, index=True)
  userId = Column(Integer, nullable=True)
  type = Column(String, nullable=True)
  provider = Column(String, nullable=True)
  providerAccountId = Column(String, nullable=True)
  refresh_token = Column(String)
  access_token = Column(String)
  expires_at = Column(Integer)
  id_token = Column(String)
  scope = Column(String)
  session_state = Column(String)
  token_type = Column(String)

class Sessions(Base):
  __tablename__ = "sessions"

  id = Column(Integer, primary_key=True, index=True)
  userId = Column(Integer, nullable=True)
  expires = Column(DateTime, nullable=True)
  sessionToken = Column(String, nullable=True)

class Users(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  email = Column(String)
  emailVerified = Column(DateTime)
  image = Column(String)


class Session(Base):
  __tablename__ = "session"

  id = Column(String, primary_key=True)
  userId = Column(Integer)
  chatHistory = Column(LargeBinary)
  active = Column(Boolean)
  result = Column(LargeBinary)
  lastActive = Column(DateTime)