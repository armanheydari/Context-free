class Main:
    from Grammer import Grammer
    n = int(input("How many variables? "))
    grammer = []
    for i in range(0, n):
        temp1 = str(input()).split(' -> ')
        if(len(temp1)==2):
            temp2 = temp1[1].split('|')
        else:
            temp1[0]=temp1[0].replace(' ->','')
            temp2=[" "]
        temp=[]
        temp.append(temp1[0])
        for j in temp2:
            temp.append(j)
        grammer.append(temp)
    myGrammer = Grammer(grammer)
    print("1=ChangeToGreibachForm\n2=ChangeToChomskyForm\n3=DeleteTrash\n4=IsGenerateByGrammer")
    n=input("What do you want?")
    if(n=='1'):
        myGrammer.ChangeToGreibachForm()
        print (myGrammer.grammer)
    if(n=='2'):
        myGrammer.ChangeToChomskyForm()
        print (myGrammer.grammer)
    if(n=='3'):
        myGrammer.DeleteTrash()
        print (myGrammer.grammer)
    if(n=='4'):
        myGrammer.IsGenerateByGrammer()

