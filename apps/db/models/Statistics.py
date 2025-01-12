from flask_login import UserMixin


class Statistics(UserMixin):

    def __init__(self, ID_Statistics  = None, Measurement_Date = None, Stature = None, Weight = None, IMC =  None, FC_Repose = None, FC_MAX = None, Blood_pressure = None, BMR = None, Body_Fat = None, Percent_Water= None, Muscle_Mass = None, Metabolic_Age = None, Bone_Mass = None, Visceral_Fat = None, Chest_Circum = None, Right_Arm_Circum = None, Left_Arm_Circum = None,Circum_Waist = None,Circum_Abdomen = None,Hip_Circum = None,Circum_Thigh_Right = None,Circum_Thigh_Left = None,Circum_Calf_Right = None, Circum_Calf_Left = None,Special_Considerations = None, sportsman = None, Training_Goal = None, Emphasis_Training = None, Disponibilidad = None,State = None, Client_ID = None, Trainer_ID = None ) -> None:
         self.ID_Statistics = ID_Statistics
         self.Measurement_Date = Measurement_Date
         self.Stature = Stature
         self.Weight = Weight
         self.IMC = IMC
         self.FC_Repose = FC_Repose
         self.FC_MAX = FC_MAX
         self.Blood_pressure = Blood_pressure
         self.BMR = BMR
         self.Body_Fat = Body_Fat
         self.Percent_Water = Percent_Water
         self.Muscle_Mass = Muscle_Mass
         self.Metabolic_Age = Metabolic_Age
         self.Bone_Mass = Bone_Mass
         self.Visceral_Fat = Visceral_Fat
         self.Chest_Circum = Chest_Circum
         self.Right_Arm_Circum = Right_Arm_Circum
         self.Left_Arm_Circum = Left_Arm_Circum
         self.Circum_Waist = Circum_Waist
         self.Circum_Abdomen = Circum_Abdomen
         self.Hip_Circum = Hip_Circum
         self.Circum_Thigh_Right = Circum_Thigh_Right
         self.Circum_Thigh_Left = Circum_Thigh_Left
         self.Circum_Calf_Right = Circum_Calf_Right
         self.Circum_Calf_Left = Circum_Calf_Left
         self.Special_Considerations = Special_Considerations
         self.sportsman = sportsman
         self.Training_Goal = Training_Goal
         self.Emphasis_Training = Emphasis_Training
         self.Disponibilidad = Disponibilidad
         self.State = State
         self.Client_ID = Client_ID
         self.Trainer_ID = Trainer_ID

            


