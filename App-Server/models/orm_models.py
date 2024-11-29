from sqlalchemy import Column, Integer, String, ForeignKey, Float, CheckConstraint
from database.database import Base
from sqlalchemy.orm import relationship


# ORM model classes (the lowest level between database and app)
# use thees classes to put and load corresponding items to database directly

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String, nullable=False)
    task_id = Column(String, nullable=False)    # task id in jira
    creation_date = Column(String, nullable=False)

    messages = relationship("Message", back_populates="task")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)    # not a foreign key - just a string value
    publication_date = Column(String)
    text = Column(String, nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    message_id = Column(String)

    task = relationship("Task", back_populates="messages")
    prediction = relationship("Prediction", back_populates="message", uselist=False)  # one-to-one relation


class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"))

    positive_prob = Column(Float, nullable=False)
    negative_prob = Column(Float, nullable=False)
    neutral_prob = Column(Float, nullable=False)

    saving_date = Column(String, nullable=False)
    conclusion = Column(String, nullable=False)
    CheckConstraint("positive_prob >= 0 and "
                    "negative_prob >= 0 and "
                    "neutral_prob >= 0 and "
                    "positive_prob <= 1 and "
                    "negative_prob <= 1 and "
                    "neutral_prob <= 1 and "
                    "ABS(positive_prob + negative_prob + neutral_prob - 1) < 0.00001", name="check_probs")

    message = relationship("Message", back_populates="prediction")
