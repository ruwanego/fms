""" Profile service

High level functions to manipulate profile data

Created by Lahiru Pathirage @ Mooniak<lpsandaruwan@gmail.com> on 22/12/2016
"""

from model import Profile
from session import db_session


class ProfileService:

    def add_new(self, user_id, email, name, password, token):
        new_profile = Profile(
            user_id=user_id,
            email=email,
            is_logged=True,
            name=name,
            password=password,
            token=token,
        )

        db_session.add(new_profile)
        db_session.commit()

        return new_profile

    def find_user(self):
        return db_session.query(Profile).first()

    def set_active_mode(self, active_mode):
        self.update_user(
            {
                "is_logged": active_mode
            }
        )

    def update_user(self, update_list):
        db_session.query(Profile).update(update_list)
        db_session.commit()
