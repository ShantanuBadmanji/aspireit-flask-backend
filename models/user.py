from app import bcrypt, mongoDB

class User:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
        self.name: str = ""
        self.age: int = 0

    def __repr__(self):
        return f"User('{self.email}', '{self.name}', '{self.age}'"

    def save(self):
        mongoDB.users.update_one(
            {"email": self.email}, {"$set": self.__dict__}, upsert=True
        )
