import lib.RTDConverter as rc
import matplotlib.pyplot as plt

if __name__ == '__main__':
    MyConverter = rc.RTDConverter()
    MyConverter.ParseRTTable("./DB/RTD100CalibrationTable.txt")
    parsed_table = MyConverter.GetParsedTable()
    #Show the table parsed properly
    plt.plot(parsed_table["R"],parsed_table["T"])
    plt.xlabel("Resistance",fontsize=20)
    plt.ylabel("Temperature",fontsize=20)
    plt.title("RTD Resistance-Temperature conversion parsed",fontsize=20)
    plt.show()
    temp_test = 293.0
    print("RESISTANCE ASSOCIATED WITH TEMP OF %f: %f."%(temp_test,MyConverter.GetResistance(temp_test)))
    r_test = 100.0
    print("RESISTANCE ASSOCIATED WITH TEMP OF %f: %f."%(r_test,MyConverter.GetTemperature(r_test)))
    print("Demo of what happens if input resistance is too low/high")
    r_test = 0.001
    print("RESISTANCE ASSOCIATED WITH TEMP OF %f: %f."%(r_test,MyConverter.GetTemperature(r_test)))
