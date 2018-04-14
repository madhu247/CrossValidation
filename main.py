import re
import CrossValidation

def main():
    print ""
    print "\t+----------------------------------------------------------------+"
    print "\t|                                                                |"
    print "\t|       CROSS VALIDATION OF LEARNING FORM EXAMPLE MODULES (LEM1) |"
    print "\t|                    RULE INDUCTION ALGORITHM                    |"
    print "\t|       Author : Madhu Chegondi                                  |"
    print "\t|       KUID   : m136c192                                        |"
    print "\t|                                                                |"
    print "\t+----------------------------------------------------------------+"
    print ""
    dataFile = raw_input("\tEnter Name Of DataFile : ")
    while (True):
        if (dataFile):
            try:
                dfp = open('Data/'+dataFile, 'r')
                # This Program assumes that first 2 lines of the input data filename have
                # < a a a d >
                # [ attribute1 attribute2 attribute3 decision ]
                header1 = dfp.readline()
                header2 = dfp.readline().strip().split()
                AttNames = header2[1:-1]
                DesName = header2[-2]
                attr = []
                decisions = []
                for line in dfp:
                    if re.match(r'^\!.*', line) or line.strip() == '':
                        continue
                    line.strip()
                    values = line.split()
                    rawData = {}
                    des = {}
                    for i in range(len(values)-1):
                        try:
                            if(type(float(values[i])) == float):
                                rawData[AttNames[i]] = float(values[i])
                        except ValueError:
                            rawData[AttNames[i]] = values[i]
                    attr.append(rawData)
                    des[DesName] = values[-1]
                    decisions.append(des.items())
                break
            except:
                print "\t\tERROR: Enter A Valid File Name\n"
                dataFile = raw_input("\tEnter Name Of DataFile : ")
        else:
            dataFile = raw_input("\tEnter Name Of DataFile : ")

    print "\n\tCROSS VALIDATION TECHNIQUES"
    print "\t\t1. BOOTSTRAP CROSS VALIDATION"
    print "\t\t2. LEAVING ONE OUT CROSS VALIDATION"
    choice  = raw_input("\n\tENTER YOUR CHOICE OF CROSS VALIDATION (1 or 2) : ")
    while True:
        if choice == '1' or choice == '2':
            break
        else:
            choice  = raw_input("\tENTER YOUR CHOICE OF CROSS VALIDATION (1 or 2) : ")


    samples = None
    if choice == '1':
        method = 'Bootstrap'
        print "\n\tCONFIGURING BOOTSTRAP"
        samples = raw_input("\t\tHow many samples do you wish to create (default 200 samples) : ")
    else:
        method = 'LeaveOneOut'

    CrossValidation.CrossValidation(attr, decisions, DesName, method, samples, dataFile)

if __name__ == '__main__':
    main()
