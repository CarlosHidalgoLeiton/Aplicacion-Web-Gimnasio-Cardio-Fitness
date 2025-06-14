from apps.db.models.Membership import Membership
from pymysql import IntegrityError

from apps.db.repositories.RepositoryBase import RepositoryBase

class MembershipRepository(RepositoryBase):

    def __init__(self):
        super().__init__(Membership)

    def getDataMembershipDay(self, membership_id):
        try:
            result = self.findOneFiltered(
                column_names=["Time"],
                filters={"id": membership_id}
            )

            if result:
                return result["Time"]
            return None
        except Exception as ex:
            print(f"Error al obtener duración de la membresía: {ex}")
            return None
    
    def getDataMembership(self,request):
            membershipId = request.form['DocumentIdMembresia']
            membership_days = self.getDataMembershipDay(membershipId)

            if membership_days is None:
                return "Tipo de membresía no encontrado"
           
            return membership_days

    @classmethod
    def getDataMembershipSent(cls, request):
        return {
            "Name": request.form['name'],
            "Description": request.form["description"],
            "Price": request.form['price'] if float(request.form['price']) else 0,
            "Time": request.form['time'] if int(request.form['time']) else 0,
            "State": True
        }

    @classmethod
    def validateDataForm(cls, membership):
        if not membership.get("Name"):
            return "Debe ingresar el nombre de la membresía."
        if not membership.get("Description"):
            return "Debe ingresar la descripción de la membresía."
        if membership.get("Price") is None or float(membership["Price"]) < 0:
            return "El precio de la membresía debe ser un número positivo."
        if membership.get("Time") is None or int(membership["Time"]) <= 0:
            return "La duración de la membresía debe ser un número mayor a cero."
        return True


    def disable_membership(self, membership_id):
        return self.update(membership_id, State=False)

    def enable_membership(self, membership_id):
        return self.update(membership_id, State=True)

