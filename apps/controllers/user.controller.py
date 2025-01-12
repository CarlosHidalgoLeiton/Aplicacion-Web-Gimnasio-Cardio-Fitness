from apps.db.repositories.UserRepository import UserRepository

class userController:

    def get_by_id(id):
        try:
            user = UserRepository.get_one(id)
        except Exception as ex:
            raise Exception(f'Error en user.controller.py {ex}')