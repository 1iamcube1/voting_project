from datetime import datetime, timedelta
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, db_connection):
        self.conn = db_connection
        self.cursor = self.conn.cursor()

    def find_by_cccd(self, cccd):
        self.cursor.execute("SELECT * FROM Users WHERE cccd = ?", (cccd,))
        row = self.cursor.fetchone()
        if row:
            columns = [column[0] for column in self.cursor.description]
            return dict(zip(columns, row))
        return None

    def create_or_update(self, cccd, otp):
        otp_expires = datetime.utcnow() + timedelta(minutes=10)
        user = self.find_by_cccd(cccd)
        if user:
            self.cursor.execute(
                "UPDATE Users SET otp = ?, otp_expires = ? WHERE cccd = ?",
                (otp, otp_expires, cccd)
            )
        else:
            raise ValueError("User does not exist. Please register first.")
        self.conn.commit()

    def verify_otp(self, cccd, otp):
        self.cursor.execute(
            "SELECT * FROM Users WHERE cccd = ? AND otp = ? AND otp_expires > ?",
            (cccd, otp, datetime.utcnow())
        )
        return self.cursor.fetchone() is not None

    @staticmethod
    def get_by_id(user_id, db_connection):
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            columns = [column[0] for column in cursor.description]
            user_data = dict(zip(columns, row))
            user = User(db_connection)
            user.id = user_data['user_id']
            user.first_name = user_data['first_name']
            return user
        return None