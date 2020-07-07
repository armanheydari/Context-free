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
        # check if the grammer is in Greibach normal form or no
        for i in self.grammer:
            j = 1
            while j != len(i):
                if i[j].count('<') > 0:
                    if i[j].startswith('<'):
                        self.isGreibachNormalForm = False
                        return self.isGreibachNormalForm

                list_i_j = list(i[j])
                for k in range(len(list_i_j)):
                    if list_i_j[k] == '>' and k + 1 != len(list_i_j):
                        if list_i_j[k+1] != '<':
                            self.isGreibachNormalForm = False
                            return self.isGreibachNormalForm
                j += 1

    def __init__(self, grammer):
        self.grammer = grammer
        self.isDeleteTrash = self.CheckDelete()
        self.isChomskyForm = self.CheckChomsky()
        self.isGreibachNormalForm = self.CheckGreibach()

    def ChangeToGreibachForm(self):
        self.DeleteTrash()
        if self.isChomskyForm == False:
            self.ChangeToChomskyForm()

        while self.CheckGreibach() == False:
            self.eliminate_left_recursion()
            for i in range(len(self.grammer)):
                production = self.grammer[i]
                j = 1
                while j != len(production):
                    rule = production[j]
                    if rule.startswith('<'):
                        self.convertToGNForm(i, j)
                        j = 0
                    j += 1

    def convertToGNForm(self, r_index, p_index):
        p = self.grammer[r_index].pop(p_index)
        r = self.grammer[r_index]
        index = p.index('>')
        var = p[:index+1]
        value = p[index+1:]
        values = self.FindValues(var)
        values_list = []

        for i in values:
            i_list = list(i)
            for j in range(len(i_list)):
                if i_list[j] == '>' and j + 1 != len(i_list):
                    if i_list[j+1] != '<':
                        values_list.append(i)
            if not i.startswith('<'):
                values_list.append(i)
        for val in values_list:
            if self.checkNotDuplicate(r[0], val) and val != var:
                r.append(val + value)

    def FindValues(self, variable):
        values = []
        for i in self.grammer:
            if i[0] == variable:
                j = 1
                while j != len(i):
                    values.append(i[j])
                    j += 1
        return values

    def checkNotDuplicate(self, variable, rule):
        for i in self.grammer:
            j = 1
            while j != len(i):
                if i[0] == variable and i[j] == rule:
                    return False
                j += 1
        return True


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

    def eliminate_left_recursion(self):
        for i in range(len(self.grammer)):
            production = self.grammer[i]
            elinimate_index = []
            elinimate_str = []
            simple_index = []
            simple_str = []
            j = 1
            while j != len(production):
                k = 0
                flag = True
                while k != len(production[j]):
                    if production[j][k] == '>' and k + 1 != len(production[j]):
                        if production[j][k+1] != '<':
                            elinimate_index.append(k)
                            elinimate_str.append(production[j])
                        else:
                            simple_index.append(k)
                            simple_str.append(production[j])
                    else:
                        simple_index.append(k)
                        simple_str.append(production[j])
                    k += 1
                j += 1

            if len(elinimate_index) > 0:
                new_var = '<NEW_' + str(production[0]) + '>'
                for j in range(len(simple_index)):
                    index = int(simple_index[j])
                    extra = simple_str[j]
                    extra = extra + new_var
                    self.grammer[i][j] = extra

                new_variable = []
                new_variable.append(new_var)
                self.grammer[0].append(new_variable)
                for j in range(len(elinimate_index)):
                    extra = elinimate_str[j]
                    index = extra.index('>')
                    extra = extra[:index+1] + new_var
                    self.grammer[-1].append(extra)
                self.grammer[-1].append('lamda')

                for j in range(len(elinimate_index)):
                    index = int(elinimate_index[j]) - j
                    self.grammer[i].pop(index)

                self.DeleteTrash()

    def IsGenerateByGrammer(self, s):
        if self.isChomskyForm:
            temp = s.split(' ')
            str_length = len(temp)
            r = len(self.grammer)
            p = [[[False for i in range(r)] for j in range(
                str_length)] for k in range(str_length)]

            for index in range(str_length):
                for i in self.grammer:
                    for value in self.FindValues(i[0]):
                        if value.count('<') == 0 and temp[index] == value:
                            p[0][index][self.grammer.index(i)] = True
                            break

            for length_span in range(1, str_length):
                for start_span in range(str_length - length_span):
                    for partition_span in range(length_span):
                        for i in self.grammer:
                            for value in self.FindValues(i):
                                if value.count('<') == 2:
                                    index = value.index('>')
                                    variable_1 = value[:index+1]
                                    variable_2 = value[index+1:]

                                    for j in self.grammer:
                                        if j[0] == variable_1:
                                            x = self.grammer.index(j)
                                            break

                                    for j in self.grammer:
                                        if j[0] == variable_2:
                                            y = self.grammer.index(j)
                                            break

                                    if p[partition_span][start_span][x] and p[length_span-partition_span-1][start_span+partition_span+1][y]:
                                        p[length_span][start_span][self.grammer.index(
                                            i)] = True

            return p[str_length-1][0][0]

        else:
            pass
