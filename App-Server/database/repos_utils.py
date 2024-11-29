from datetime import datetime
from sqlalchemy.orm import Session
from models.dto_models import TaskCreateDTO, MessageCreateDTO, PredictionCreateDTO
from models.orm_models import Task, Message, Prediction


def save_task(db: Session, taskCreateDTO: TaskCreateDTO):
    db_task = Task(task_name=taskCreateDTO.task_name, task_id=taskCreateDTO.task_id,
                   creation_date=str(taskCreateDTO.creation_date))
    db.add(db_task)
    db.commit()
    db.refresh(db_task)  # update db_task object from database

    return db_task


def get_task_by_task_id(db: Session, task_id: str):
    result = db.query(Task).filter(Task.task_id == task_id).first()

    return result


def get_task_by_id(db: Session, id: int):
    result = db.query(Task).filter(Task.id == id).first()

    return result


def update_task(db: Session, id: int, taskCreateDTO: TaskCreateDTO):
    db.query(Task).filter(Task.id == id).update({"task_name": taskCreateDTO.task_name})
    db.commit()

    return get_task_by_id(db, id)  # return updated task


def save_message(db: Session, messageCreateDTO: MessageCreateDTO, task_id: int):
    db_message = Message(user_id=messageCreateDTO.user_id, publication_date=str(messageCreateDTO.publication_date),
                         text=messageCreateDTO.text, task_id=task_id, message_id=messageCreateDTO.message_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return db_message


def get_message_by_message_id(db: Session, message_id: str):
    return db.query(Message).filter(Message.message_id == message_id).first()


def get_message_by_id(db: Session, id: int):
    return db.query(Message).filter(Message.id == id).first()


def update_message(db: Session, id: int, messageCreateDTO: MessageCreateDTO):
    db.query(Message).filter(Message.id == id).update({"text": messageCreateDTO.text,
                                                       "user_id": messageCreateDTO.user_id}
                                                      )
    db.commit()

    return get_message_by_id(db, id)


def save_text(db: Session, messageCreateDTO: MessageCreateDTO):
    db_message = Message(text=messageCreateDTO.text)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return db_message


def save_prediction(db: Session, predictionCreateDTO: PredictionCreateDTO, message_id: int):
    saving_date = datetime.now()
    db_prediction = Prediction(positive_prob=predictionCreateDTO.positive_prob,
                               negative_prob=predictionCreateDTO.negative_prob,
                               neutral_prob=predictionCreateDTO.neutral_prob,
                               conclusion=predictionCreateDTO.conclusion,
                               saving_date=str(saving_date), message_id=message_id)
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)

    return db_prediction


def get_prediction_by_message_id(db: Session, message_id: int):
    return db.query(Prediction).filter(Prediction.message_id == message_id).first()


def update_prediction(db: Session, predictionCreateDTO: PredictionCreateDTO, message_id: int):
    saving_date = datetime.now()
    db.query(Prediction).filter(Prediction.message_id == message_id) \
        .update({"positive_prob": predictionCreateDTO.positive_prob,
                 "negative_prob": predictionCreateDTO.negative_prob,
                 "neutral_prob": predictionCreateDTO.neutral_prob,
                 "conclusion": predictionCreateDTO.conclusion,
                 "saving_date": str(saving_date)
                 })
    db.commit()

    return get_prediction_by_message_id(db, message_id)
