import sys
def encoding():
    opcode={"add":"10000","sub":"10001","ld":"10100","st":"10101","mul":"10110","div":"10111","ls":"11001","rs":"11000","xor":"11010","or":"11011","and":"11100","not":"11101","cmp":"11110","jmp":"11111","jlt":"01100","jgt":"01101","je":"01111","hlt":"01010","movim":"10010","movr":"10011"}
    return opcode
def getKeywords():
    keywords=["add","sub","ld","st","mul","div","ls","rs","xor","or","and","not","cmp","jmp","jlt","jgt","je","hlt","mov","var","FLAGS","r0","r1","r2","r3","r4","r5","r6","R0","R1","R2","R3","R4","R5","R6"]
    return keywords
def LABL(d,index,lins,v):
    labels=dict()
    variables=dict()
    keywords=getKeywords()
    z=0
    for lineno in range(len(d)):
        if ":" in "".join(d[lineno]):
            if len("".join(d[lineno]).split(":"))<3 and "".join(d[lineno]).split(":")[1]=='':
                print(f"Error at line no {index[lineno]+1}: Label does not start in the same line")
                exit(0)
            elif(":" not in d[lineno][0] or d[lineno][0].strip()==":"):
                print(f"Error at line no {index[lineno]+1}: Invalid label name")
                exit(0)
            elif(" :" in d[lineno][0]):
                print(f"Error at line no {index[lineno]+1}: Space between label and ':'")
                exit(0)
            elif(": " not in " ".join(d[lineno])):
                print(f"Error at line no {index[lineno]+1}: No space after ':'")
                exit(0)
            else:
                if("".join(d[lineno]).count(":")>1):
                    print(f"Error at line no {index[lineno]+1}: invalid nested label")
                    exit(0)
                t=" ".join(d[lineno]).split(":")
                d[lineno]=t[1].split()
                if (t[0] in keywords): 
                    print(f"Error at line no {index[lineno]+1}: Use of keyword as label name not allowed")
                    exit(0)
                elif (t[0] in labels):
                    print(f"Error at line no {index[lineno]+1}: label name already used")
                    exit(0)
                elif(t[0] in variables):
                    print(f"Error at line no {index[lineno]+1}: variable used as label name")
                    exit(0)
                elif(not t[0].isalnum()):
                    print(f"Error at line no {index[lineno]+1}: label name should be alphanumeric")
                    exit(0)
                labels[t[0]]=str((lineno)-len(variables))
        elif "var" in "".join(d[lineno])[0:3]:
            if(len(d[lineno])>2 or len(d[lineno])==1):
                print(f"Error at line no {index[lineno]+1}: invalid variable syntax")
                exit(0)
            if(d[lineno]==['var', 'var']):
                print(f"Error at line no {index[lineno]+1}: Use of keyword as variable name not allowed")
                exit(0)
            t=" ".join(d[lineno])[4:]
            if (t in keywords): 
                print(f"Error at line no {index[lineno]+1}: Use of keyword as variable name not allowed")
                exit(0)
            elif(t in variables):
                print(f"Error at line no {index[lineno]+1}: variable name already used")
                exit(0)
            elif(t in labels):
                print(f"Error at line no {index[lineno]+1}: label name used as variable name") 
                exit(0)
            elif((not t.isalnum())):
                    print(f"Error at line no {index[lineno]+1}: variable name should be alphanumeric")
                    exit(0)
            variables[t]=str((lins-v+z))
            z+=1
    return [labels,variables]
def takeInput():
    d=sys.stdin.readlines()
    instructions=[]
    index=[]
    h=0
    v=0
    for i in range(len(d)):
        if (d[i].split()!=[]):
            instructions.append(d[i].strip().split())
            if("".join(instructions[-1])[0:3]=="var"):
                v+=1
            index.append(i)
        if("hlt" in d[i]):
            if(i<len(d)-1):
                h=1
                print(f"Error at line no {i+1}: hlt not at end of program")
                exit(0)
            elif(h==1):
                print("More than one hlt")
                exit(0)
            else:
                h=1
    if(h==0):
        print("Error: missing hlt instruction")
        exit(0)
    i=0
    labels,variables=LABL(instructions,index,len(instructions),v)
    while i<len(instructions):
        if (instructions[i][0]=="var"):
            instructions.append(instructions.pop(0))
            index.append(index.pop(0))
        else:
            break
    return [instructions,labels,variables,index]
def encodeRegister():
    reg={"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100","R5":"101", "R6":"110","FLAGS":"111","r0":"000","r1":"001", "r2":"010", "r3":"011", "r4":"100","r5":"101", "r6":"110"}
    return reg
def findType():
    instructionType={"add":'A',"sub":'A',"mul":'A',"xor":'A',"or":'A',"and":'A','movim':'B',"rs":"B","ls":"B","movr":"C","div":"C","not":"C","cmp":"C","ld":"D","st":"D","jmp":"E","jlt":"E","jgt":"E","je":"E","hlt":"F"}
    return instructionType
def findUnused():
    unusedBits={'A':"00",'C':"00000","E":"000","F":"00000000000"}
    return unusedBits
def error(instruction,index,count):
    opcode=encoding()
    if instruction[0]=="var":
        return (f"Error at line no {index[count]+1}: variable not declared in starting")
    elif instruction[0] not in opcode:
        return (f"Error at line no {index[count]+1}: {instruction[0]} is not a valid operation.")
    elif (instruction[0]!="movr") and ("FLAGS" in instruction):
        return (f"Error at line no {index[count]+1}: Illegal use of flag register.")
    elif (instruction[0]=="movr") and (instruction[2]=="FLAGS"):
        return (f"Error at line no {index[count]+1}: Illegal use of flag register.")
    return "0"
def convert(immediateValue):
    if not immediateValue.isdigit():
        return -2
    immediateValue=int(immediateValue)
    if(immediateValue>255 or immediateValue<0):
        return -1
    immediateValue=bin(immediateValue)
    immediateValue=str(immediateValue)
    immediateValue=immediateValue[2:]
    immediateValue=immediateValue[::-1]
    bits=8-len(immediateValue)
    j=1
    while j<=bits:
        immediateValue+='0' 
        j=j+1
    immediateValue=immediateValue[::-1]
    return immediateValue   

def main():
    opcode=encoding()
    unusedBits=findUnused()
    instructionType=findType()
    reg=encodeRegister()
    keywords=getKeywords()
    instructions,labels,variables,index=takeInput()
    encoded=[]
    count=0
    for i in instructions:
        if i[0]=="mov" and len(i)!=3:
            print(f"Error at line no {index[count]+1}: Invalid Syntax of mov instruction.")
            exit(0)
        if i[0]=="mov":
            if i[2][0]=="$":
                i[0]+="im"
            elif i[2][0]=="R" or i[2][0]=="r" or i[1]=="FLAGS":
                i[0]+="r"
            elif i[2]=="FLAGS":
                print(f"Error at line no {index[count]+1}: Illegal use of flag register.")
                exit(0)
            else:
                print(f"Error at line no {index[count]+1}: Invalid Syntax for {i[0]} instruction")
                exit(0)
        z=error(i,index,count)
        if(z!="0"):
            print(z)
            exit(0)
        encode=""
        encode+=opcode[i[0]]
        if instructionType[i[0]]=="A":
            if len(i)!=4:
                print(f"Error at line no {index[count]+1}: Invalid Syntax of instruction Type {i[0]}")
                exit(0)
            try:
                encode+=unusedBits[instructionType[i[0]]]+reg[i[1]]+reg[i[2]]+reg[i[3]]
            except Exception as e:
                e=str(e)[1:len(str(e))-1]
                if e in keywords:
                    print(f"Error at line no {index[count]+1}: Illegal use of keyword {e}")
                else:
                    print(f"Error at line no {index[count]+1}: The register {e} is invalid.")
                exit(0)
        elif instructionType[i[0]]=="B":
            if len(i)!=3:
                print(f"Error at line no {index[count]+1}: Invalid Syntax of instruction Type {i[0]}")
                exit(0)
            try:
                immediateValue=i[2][1:]
                immediateValue=convert(immediateValue)
                if(immediateValue==-1):
                    print(f"Error at line no {index[count]+1}: The immediate value is out of range")
                    exit(0)
                if(immediateValue==-2):
                    print(f"Error at line no {index[count]+1}: Immediate value must be a whole number")
                    exit(0)
                encode+=reg[i[1]]+immediateValue
            except Exception as e:
                e=str(e)[1:len(str(e))-1]
                if e in keywords:
                    print(f"Error at line no {index[count]+1}: Illegal use of keyword {e}")
                else:
                    print(f"Error at line no {index[count]+1}: The register {e} is invalid")   
                exit(0) 
        elif instructionType[i[0]]=="C":
            if len(i)!=3:
                print(f"Error at line no {index[count]+1}: Invalid Syntax of instruction Type {i[0]}")
                exit(0)
            try:
                encode+=unusedBits[instructionType[i[0]]]+reg[i[1]]+reg[i[2]]
            except Exception as e:
                e=str(e)[1:len(str(e))-1]
                if e in keywords:
                    print(f"Error at line no {index[count]+1}: Illegal use of keyword {e}")
                else:
                    print(f"Error at line no {index[count]+1}: The register {e} is invalid") 
                exit(0)  
        elif instructionType[i[0]]=="D":
            if(len(i)!=3):
                print(f"Error at line no {index[count]+1}: Invalid Syntax of instruction {i[0]}")
                exit(0)
            if ((i[1] in keywords)and(i[1] not in reg)) or (i[2] in keywords):
                print(f"Error at line no {index[count]+1}: Illegal use of keyword")
                exit(0)
            if i[1] not in reg.keys():
                print(f"Error at line no {index[count]+1}: The register {i[1]} is invalid")
                exit(0)
            if i[2] not in variables.keys():
                print(f"Error at line no {index[count]+1}: Variable {i[2]} not declared")
                exit(0)
            memAddress=variables[i[2]]
            memAddress=convert(memAddress)
            encode+=reg[i[1]]+memAddress
        elif instructionType[i[0]]=="E":
            if(len(i))!=2:
                print(f"Error at line no {index[count]+1}: Invalid Syntax of instruction Type {i[0]}")
                exit(0)
            if i[1] in keywords:
                print(f"Error at line no {index[count]+1}: Invalid use of keyword as label")
                exit(0)
            if(i[1] not in labels):
                print(f"Error at line no {index[count]+1}: Label {i[1]} does not exist")
                exit(0)
            
            memAddress=labels[i[1]]
            memAddress=convert(memAddress)
            encode+=unusedBits[instructionType[i[0]]]+memAddress
        elif instructionType[i[0]]=="F":
            if(len(i)!=1):
                print(f"Error at line no {index[count]+1}: Invalid Syntax of instruction Type {i[0]}")
                exit(0)
            encode+=unusedBits[instructionType[i[0]]]
            break
        count+=1
        encoded.append(encode)
    encoded.append(encode)
    for i in encoded:
        print(i)
main()
