"""
from datetime import datetime

from django.contrib.sessions.backends.db import SessionStore as DBStore

import models


class SessionStore(DBStore):

    @classmethod
    def get_model_class(cls):
        return models.Sesion

    def create_model_instance(self, data):
        obj = super(SessionStore, self).create_model_instance(data)
        try:
            user_id = int(data.get('_auth_user_id'))
            obj.horaUltimoAcceso = datetime.now()

        except (ValueError, TypeError):
            user_id = None
        obj.user_id = user_id
        return obj

"""