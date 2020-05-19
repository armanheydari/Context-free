class Grammer:
    def __init__(self,grammer):
        self.grammer=grammer
        #check is it chomsky
        self.isChomskyForm = False
        
        #check is it Greibach
        self.isGreibachNormalForm = False
        
        self.isDeleteTrash = False
        for i in grammer:
            if self.isDeleteTrash == False and "lamda" in i:
                self.isDeleteTrash=True
        for i in grammer:
            for j in i:
                print(j.split('<'))
        


    def ChangeToGreibachForm(self):
        pass

    def ChangeToChomskyForm(self):
        pass

    def DeleteTrash(self):
        pass

    def IsGenerateByGrammer(self):
        pass
