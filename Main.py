class Main:
    from Grammer import Grammer
    n = int(input("How many variables? "))
    grammer = {}
    for i in range(0, n):
        temp = str(input()).split(' -> ')
        if(len(temp)==2):
            grammer[temp[0]] = temp[1].split('|')
        else:
            grammer[temp[0]] = " "
    myGrammer = Grammer(grammer)
    print("1=ChangeToGreibachForm\n2=ChangeToChomskyForm\n3=DeleteTrash\n4=IsGenerateByGrammer")
    n=input("What do you want?")
    if(n=='1'):
        myGrammer.ChangeToGreibachForm
    if(n=='2'):
        myGrammer.ChangeToChomskyForm
    if(n=='3'):
        myGrammer.DeleteTrash
    if(n=='4'):
        myGrammer.IsGenerateByGrammer

