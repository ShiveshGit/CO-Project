def binary(immediateValue):
    temp=int(immediateValue)
    temp=bin(temp)
    temp=str(temp)
    temp=temp[2:]
    return temp
def binary_after(immediateValue,bits):
    exponent="."+immediateValue
    lenExponent=len(immediateValue)
    j=1
    temp=""
    while(float(exponent)!=0 and j<=bits):
        exponent=("{:1.5f}".format(float(exponent)*2)).split(".")
        expo=exponent[0]
        exponent="."+exponent[1]
        temp+=expo
        j+=1
    z=0
    for i in range(1,len(temp)+1):
        z=z+int(temp[i-1])*(2**(-i))
    imm1=immediateValue.lstrip("0.")
    z=str(z).lstrip("0.")

    if str(z)!=imm1:
        return 1
    return temp
def ieee(immediateValue,i=0):
    flag=0
    immediateValue=immediateValue.split(".")
    if(len(immediateValue)!=2 or immediateValue[-1]==''):
        print(f"Error at line no {i}: Invalid floating point value")
        exit(0)
    elif float(".".join(immediateValue))>252.0:
        print(f"Error at line no {i}: The value is greater than max value which can be allowed in register")
        exit(0)
    elif float(".".join(immediateValue))<1.0:
        print(f"Error at line no {i}: The value is lesser than min value which can be allowed in register")
        exit(0)
    beforeDecimal=binary(immediateValue[0])
    immediateValue[1]=list(immediateValue[1])
    while len(immediateValue[1])>1:
        if(immediateValue[1][-1]=="0"):
            immediateValue[1].pop()
        else:
            break
    immediateValue[1]="".join(immediateValue[1])
    if(len(immediateValue[1])>5):
        return 1
    afterDecimal=binary_after(immediateValue[1],5)
    if afterDecimal==1:
        return 1
    l=".".join([beforeDecimal,afterDecimal])
    exponent=l.find(".")-1
    exponent="{:03b}".format(exponent)
    mantissa=list("".join(l[1:].split(".")))
    while len(mantissa)>0:
        if mantissa[-1]=="0":
            mantissa.pop()
        else:
            break
    mantissa="".join(mantissa)
    bheloo=exponent+mantissa
    x=len(bheloo)
    if x<8:
        for i in range(x,8):
            bheloo+="0"
    elif(x>8):
        flag=1
        return 1    
    return bheloo
