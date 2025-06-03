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

    @classmethod
    def get_all(cls, filters=None):
        memberships = cls.MembershipRepository.findAll(filters)
        if not memberships:
            raise Exception('No se encontraron membresías')
        return memberships

    @classmethod
    def get_by_id(cls, membership_id):
        membership = cls.MembershipRepository.get_one(membership_id)
        if not membership:
            raise Exception(f'Membresía con ID {membership_id} no encontrada')
        return cls.MembershipRepository.to_dict(membership)

    @classmethod
    def create_membership(cls, data):
        try:
            new_membership = cls.MembershipRepository.create(**data)
            return cls.MembershipRepository.to_dict(new_membership)
        except Exception as e:
            raise Exception(f"Error al crear la membresía: {str(e)}")

    @classmethod
    def update_membership(cls, membership_id, data):
        try:
            updated = cls.MembershipRepository.update(membership_id, **data)
            return cls.MembershipRepository.to_dict(updated)
        except Exception as e:
            raise Exception(f"Error al actualizar la membresía: {str(e)}")

    @classmethod
    def getDataMembership(cls, request):
        return cls.MembershipRepository.getDataMembership(request)

    @classmethod
    def membershipValidated(cls, membership):
        return cls.MembershipRepository.validateDataForm(membership)


    @classmethod
    def disable_membership(cls, membership_id):
        try:
            return cls.MembershipRepository.disable_membership(membership_id)
        except Exception as e:
            raise Exception(f"Error al deshabilitar la membresía: {str(e)}")

    @classmethod
    def enable_membership(cls, membership_id):
        try:
            return cls.MembershipRepository.enable_membership(membership_id)
        except Exception as e:
            raise Exception(f"Error al habilitar la membresía: {str(e)}")
