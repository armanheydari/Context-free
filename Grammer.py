class Grammer:
    def CheckDelete(self):
        self.isDeleteTrash = False
        # check nullables
        for i in self.grammer:
            if self.isDeleteTrash == False and "lamda" in i:
                self.isDeleteTrash = True
        # check unit productions
        for i in self.grammer:
            for j in i[1:len(i)]:
                if self.isDeleteTrash == False and j.isupper() and not '<' in j[1:len(j)]:
                    self.isDeleteTrash = True
        # check useless productions:
        v = []
        temp = True
        v.append(self.grammer[0][0])
        while temp and self.isDeleteTrash == False:
            temp = False
            for i in self.grammer:
                for j in i[1:len(i)]:
                    k = 0
                    while k in range(0, len(j)):
                        s = ""
                        if j[k] == '<':
                            while j[k] != '>':
                                s = s+j[k]
                                k = k+1
                            s = s+'>'
                            if not s in v:
                                v.append(s)
                                temp = True
                        k = k+1
        if self.isDeleteTrash == False:
            for i in self.grammer:
                if not i[0] in v:
                    self.isDeleteTrash = True
        if self.isDeleteTrash == False:
            for i in self.grammer:
                for j in i[1:len(i)]:
                    if j.islower() and not j in v:
                        v.append(i[0])
        temp = True
        while temp and self.isDeleteTrash == False:
            temp = False
            for i in self.grammer:
                for j in v:
                    for k in i[1:len(i)]:
                        if j in k and not i[0] in v:
                            v.append(i[0])
                            temp = True
        if self.isDeleteTrash == False:
            for i in self.grammer:
                if not i[0] in v:
                    self.isDeleteTrash = True
        return self.isDeleteTrash

    def CheckChomsky(self):
        self.isChomskyForm = True
        # check if the grammer is in chomsky normal form or no
        for i in self.grammer:
            for j in i:
                if self.isChomskyForm == True and not j.isupper() and len(j) > 1:
                    self.isChomskyForm = False
        for i in self.grammer:
            for j in i:
                if self.isChomskyForm == True and j.count("<") > 2:
                    self.isChomskyForm = False
        return self.isChomskyForm

    def CheckGreibach(self):
        self.isGreibachNormalForm = False
        # check if the grammer is in Greibach normal form or no

        return self.isGreibachNormalForm

    def __init__(self, grammer):
        self.grammer = grammer
        self.isDeleteTrash = self.CheckDelete()
        self.isChomskyForm = self.CheckChomsky()
        self.isGreibachNormalForm = self.CheckGreibach()

    def ChangeToGreibachForm(self):
        pass

    def ChangeToChomskyForm(self):
        self.DeleteTrash()
        # change terminals to T variables
        iNumber = 0
        for i in self.grammer:
            jNumber = 0
            for j in i:
                if not j.isupper() and len(j) > 1:
                    k = 0
                    while k < len(j):
                        if j[k].islower():
                            temp1 = '<T'+j[k].upper()+'>'
                            temp = True
                            for l in self.grammer:
                                if l[0] == temp1:
                                    temp = False
                            if temp:
                                self.grammer.append([temp1, j[k]])
                            self.grammer[iNumber][jNumber] = j.replace(
                                j[k], temp1)
                            i[jNumber] = j.replace(j[k], temp1)
                            j = j.replace(j[k], temp1)
                        k = k+1
                jNumber = jNumber+1
            iNumber = iNumber+1
        # add V variables
        index = 1
        iNumber = 0
        for i in self.grammer:
            jNumber = 0
            for j in i:
                if j.count("<") > 2:
                    newVariable = '<V'+str(index)+'>'
                    index = index+1
                    k = 0
                    while not j[k] == '>':
                        k = k+1
                    k = k+1
                    newGrammer = j[k:len(j)]
                    self.grammer[iNumber][jNumber] = j[0:k]+newVariable
                    self.grammer.append([newVariable, newGrammer])
                jNumber = jNumber + 1
            iNumber = iNumber + 1

    def DeleteTrash(self):
        while self.CheckDelete():
            # delete nullable:
            for i in self.grammer:
                for j in i:
                    if(j == "lamda"):
                        i.remove("lamda")
                        delVariable = i[0]
                        for k in self.grammer:
                            for l in k[1:len(k)]:
                                if(delVariable in l):
                                    k.append(l.replace(delVariable, ''))
            # delete unit productions:
            for i in self.grammer:
                for j in i[1:len(i)]:
                    if j.isupper() and not '<' in j[1:len(j)]:
                        i.remove(j)
                        for k in self.grammer:
                            if(k[0] == j):
                                for l in k[1:len(k)]:
                                    if not l in i:
                                        i.append(l)
            # delete useless productions
            v = []
            temp = True
            v.append(self.grammer[0][0])
            while temp:
                temp = False
                for i in self.grammer:
                    for j in i[1:len(i)]:
                        k = 0
                        while k in range(0, len(j)):
                            s = ""
                            if j[k] == '<':
                                while j[k] != '>':
                                    s = s+j[k]
                                    k = k+1
                                s = s+'>'
                                if not s in v:
                                    v.append(s)
                                    temp = True
                            k = k+1
            nonReachables = []
            for i in self.grammer:
                if not i[0] in v:
                    nonReachables.append(i[0])
            i = 0
            while i in range(0, len(self.grammer)):
                if self.grammer[i][0] in nonReachables:
                    self.grammer.pop(i)
                else:
                    i = i+1
            v = []
            for i in self.grammer:
                for j in i[1:len(i)]:
                    if not i[0] in v and (j.islower() or j == ' '):
                        v.append(i[0])
            temp = True
            while temp:
                temp = False
                for i in self.grammer:
                    for j in v:
                        for k in i[1:len(i)]:
                            if j in k and not i[0] in v:
                                v.append(i[0])
                                temp = True
            nonTerminals = []
            for i in self.grammer:
                if not i[0] in v:
                    nonTerminals.append(i[0])
            i = 0
            while i in range(0, len(self.grammer)):
                if self.grammer[i][0] in nonTerminals:
                    self.grammer.pop(i)
                else:
                    i = i+1
            for i in range(0, len(self.grammer)):
                j = 0
                temp = True
                while j < len(self.grammer[i]):
                    for k in nonTerminals:
                        if k in self.grammer[i][j]:
                            self.grammer[i].pop(j)
                            temp = False
                    if temp:
                        j = j+1

    def IsGenerateByGrammer(self,string):
        if self.isChomskyForm:
            
        else:

