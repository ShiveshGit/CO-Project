import math
def findAddress(addr,default=False,bits=0):
    if addr.lower()=="bit":
        totalBits=1
    elif addr.lower()=="nibble":
        totalBits=4
    elif addr.lower()=="byte":
        totalBits=8
    elif addr.lower()=="word":
        if default==False:
            cpu=int(input("Enter the number of bits your CPU has: "))
            totalBits=cpu
        else:
            totalBits=bits
    else:
        print("Please enter a valid choice")
    address=totalISA//totalBits   
    return address
mem=input("Enter the total space in the memory : ")
mem=mem.split()

number=int(mem[0])
memType=mem[1] 
check=False
cpu=0
if memType=="b":
    totalISA=number
elif memType=="B":
    totalISA=number*8
elif memType=="kb" or memType=="Kb":
    totalISA=number*1024
elif memType=="kB" or memType=="KB":
    totalISA=number*(1024)*8
elif memType=="Mb":
    totalISA=int(number*(2**20))
elif memType=="MB":
    totalISA=int(number*(2**20)*8)
elif memType=="Gb":
    totalISA=int(number*(2**30))
elif memType=="GB":
    totalISA=int(number*(2**30)*8)
elif memType=="kWord" or memType=="KWord":
    cpu=int(input("Enter the number of bits your CPU has : "))
    totalISA=int(number*(1024)*cpu)
    check=True
elif memType=="MWord":
    cpu=int(input("Enter the number of bits your CPU has : "))
    totalISA=int(number*(2**20)*cpu)
    check=True
elif memType=="GWord":
    cpu=int(input("Enter the number of bits your CPU has : "))
    totalISA=int(number*(2**30)*cpu)
    check=True
print("4 types of addressability modes of memory:- ")
print("1) Bit (Bit Adderessable Memory -Cell Size= 1 bit) ")
print("2) Nibble (Nibble Addressable Memory - Cell Size = 4 bit)")
print("3) Byte (Byte Adressable Memory - Cell Size = 8 bits)")
print("4) Word (Word Addreessable Memory - Cell Size = Word Size (depends on CPU))")
addr=input("Enter the addressability of the memory : ")
if(addr==""):
    addr="Byte"
address=findAddress(addr,check,cpu)
address=math.log2(address)
address=math.ceil(address)    
print("--------- Memory Mumbo Jumbo Menu --------")
print("1) ISA and Instruction Related query")
print("2) System Enchancement Related query")
choice=int(input("Enter the query (1 or 2): "))
if choice==1:
    print("<----------ISA and Instruction Related Queries---------->")
    print("The two types of instructions suppoerted by the ISA :-")
    print("Type A: <Q bit opcode><P bit address><x bit register>")
    print("Type B: <Q bit opcode><R bits filler><x bit register> ")
    lengthIns=int(input("Enter the length of one instruction in bits : "))
    lengthReg=int(input("Enter the length of register in bits : "))

    opcode=lengthIns-(address+lengthReg)
    if opcode<=0:
        print("Invalid input for the length of instruction since the number of bits for op-code cannot be negative")
        exit(0)
    fillerBits=lengthIns-(2*lengthReg+opcode) 
    numberofReg=int(2**lengthReg) 
    numberofInst=int(2**opcode)
    print("Minimum bits needed to represent an address in this architecture (P) = ",address)
    print("Number of bits needed by op-code = ",opcode)
    print("Number of filler bits in instruction type 2 = ",fillerBits)
    print("Maximum number of instructions, ISA can support = ",numberofInst)
    print("Maximum number of registers this ISA can support = ",numberofReg)
elif choice==2:
    print("<------------ System Enhancement Related query ----------------->")
    print("Type 1) Number of address pins needed")
    print("Type 2) Size of main memory")
    type=int(input("Enter the type of query (1 or 2): "))
    if type==1:
        print("<---------Type 1) : Number of address pins needed/saved--------->")
        bits=int(input("Enter the number of cpu bits : "))  
        addressabilityOptions={"Bit":"(Bit Adderessable Memory -Cell Size= 1 bit)","Nibble":"(Nibble Addressable Memory - Cell Size = 4 bit)","Byte":"(Byte Adressable Memory - Cell Size = 8 bits)","Word":"(Word Addreessable Memory - Cell Size = Word Size (depends on CPU))"}  #Dictionary for storing the addessability of the memory
        print("How would you like to change the addressability of the memory ?")
        z=0
        for i in addressabilityOptions:
            if(addr!=i):
                print(f"{z})",i,addressabilityOptions[i])
                z+=1
        addr1=input("Enter the new addressability of the memory : ")
        if(addr1=="Word"):
            addressNew=findAddress(addr1,True,bits)
        else:
            addressNew=findAddress(addr1,False,0)
        addressNew=math.log2(addressNew)
        addressNew=math.ceil(addressNew)
        pins=addressNew-address
        if pins<=0:
            print(f"{pins} ({-pins} pins saved) [{address} pins-> {addressNew} pins]")
        else:
            print(f"{pins} (+ {pins} pins required) [{address} pins-> {addressNew} pins]")
    elif type==2:
        print("<------------------Type 2) Size of Main Memory----------------------------->")
        bits=int(input("Enter the number of bits the CPU has : "))
        addressPins=int(input("Enter the number of address pins the CPU has : "))
        print("4 types of addressability modes of memory:- ")
        print("1) Bit (Bit Adderessable Memory -Cell Size= 1 bit) ")
        print("2) Nibble (Nibble Addressable Memory - Cell Size = 4 bit)")
        print("3) Byte (Byte Adressable Memory - Cell Size = 8 bits)")
        print("4) Word (Word Addreessable Memory - Cell Size = Word Size (depends on CPU))")
        addr2=input("Enter the addressability of the memory : ")
        totalRows=(addressPins)
        totalBits=0
        if addr2.lower()=="bit":
            totalBits=1
        elif addr2.lower()=="nibble":
            totalBits=2
        elif addr2.lower()=="byte":
            totalBits=3
        elif addr2.lower()=="word":
            totalBits=math.log2(bits)
            totalBits=math.ceil(totalBits)
        else:
            print("Please enter a valid input")
        totalBits+=addressPins
        if(totalBits>=34):
            totalBits=totalBits%33
            print(f"{2**totalBits} GB")
        elif totalBits>=24 and totalBits<=33:
            totalBits=totalBits%23
            print(f"{2**totalBits} MB")
        elif totalBits>=14 and totalBits<=23:
            totalBits=totalBits%13
            print(f"{2**totalBits} kB")
        elif totalBits>=1 and totalBits<=13:
            totalBits=totalBits%3
            print(f"{2**totalBits} B")    
    else:
        print("Please enter a valid type of query (1 or 2) for system enhancement")
else:
    print("Please enter a valid choice")