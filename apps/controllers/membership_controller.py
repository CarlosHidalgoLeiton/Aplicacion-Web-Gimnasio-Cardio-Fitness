from apps.db.repositories.MembershipRepository import MembershipRepository


class membershipController:
    MembershipRepository =  MembershipRepository()


    @classmethod
    def get_allAble(cls):
        filters = {'State': True}
        memberships = cls.MembershipRepository.findAll(filters=filters)
        if not memberships:
            raise Exception('No se encontraron membresías')
        return memberships
    @classmethod
    def validateDataFormTrainer(cls,data):
        validate = cls.MembershipRepository.validateDataFormTrainer(data)
        return validate

