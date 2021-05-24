import numpy as np

class RTDConverter(object):
    '''
    Simple class for converting from an RTD resistance reading to it's temperature, and vice
    versa. Parses a simple space-delimited table with resistance in column 1 and temperature in
    Kelvin in column 2.
    '''
    def __init__(self,temp_resistance_dict = None):
        self.resistance_temp_dict = temp_resistance_dict

    def ParseRTTable(self,path_to_table):
        '''
        Given a file path to a simple tab-delimited table, parses a resistance-temperature table into a 
        dictionary that can be used by other methods in the class.  The first line of
        the text file is assumed to be the colume labels, and should be either "T" (temperature) or
        "R" (resistance).

        Inputs:
            path_to_table [string]
            File path to the tab-delimited table text file.
        '''
        with open(path_to_table,"r") as f:
            thelines = f.readlines()
            data_dict = {}
            entry_index_dict = {}
            for j,line in enumerate(thelines):
                line = line.rstrip("\n")
                entries = line.split("\t")
                if j == 0: #Title line
                    for l,entry in enumerate(entries):
                        data_dict[entry] = []
                        entry_index_dict[l] = entry
                else:
                    for l,entry in enumerate(entries):
                        data_dict[entry_index_dict[l]].append(float(entry))
        for entry in data_dict:
            data_dict[entry] = np.array(data_dict[entry])
        self.resistance_temp_dict = data_dict

    def GetParsedTable(self):
        '''
        Returns the table parsed after running the ParseRTTable() method.
        '''
        return self.resistance_temp_dict

    def GetTemperature(self, resistance):
        '''
        Based on the currently parsed temperature-resistance table, return the temperature associated
        with the input resistance.  Simple linear extrapolation is done to get the best-fit temperature.

        Inputs:
            resistance (float)
        '''
        if resistance > np.max(self.resistance_temp_dict["R"]):
            print("ERROR: Requested temperature fit is not bounded by current table (input resistance too high)")
            print("Min R for table: " + str(self.resistance_temp_dict["R"][0]))
            print("Max R for table: " + str(self.resistance_temp_dict["R"][-1]))
            print("Returning max temperature available")
            return np.max(self.resistance_temp_dict["T"])
        resistance_range_indices = np.where(self.resistance_temp_dict["R"]<resistance)[0]
        if len(resistance_range_indices) == 0:
            print("ERROR: Requested temperature fit is not bounded by current table (input resistance too low)")
            print("Min R for table: " + str(self.resistance_temp_dict["R"][0]))
            print("Max R for table: " + str(self.resistance_temp_dict["R"][-1]))
            print("Returning min temperature available")
            return np.min(self.resistance_temp_dict["T"])
        lower_resistance_index = resistance_range_indices[-1]
        resistances_either_side = self.resistance_temp_dict["R"][lower_resistance_index:lower_resistance_index+2]
        temps_either_side = self.resistance_temp_dict["T"][lower_resistance_index:lower_resistance_index+2]
        slope = (temps_either_side[1] - temps_either_side[0])/(resistances_either_side[1] - resistances_either_side[0])
        b = temps_either_side[0] - (slope * resistances_either_side[0])
        temp_fit = slope*resistance + b
        return temp_fit

    def GetResistance(self, temperature):
        '''
        Based on the currently parsed temperature-resistance table, return the resistance associated
        with the input temperature.  Simple linear extrapolation is done to get the best-fit resistance.
        Inputs:
            temperature (float)
        '''
        if temperature > np.max(self.resistance_temp_dict["T"]):
            print("ERROR: Requested resistance fit is not bounded by current table (input temperature too high)")
            print("Min T for table: " + str(self.resistance_temp_dict["T"][0]))
            print("Max T for table: " + str(self.resistance_temp_dict["T"][-1]))
            print("Returning max resistance available")
            return np.max(self.resistance_temp_dict["R"])
            return
        resistance_range_indices = np.where(self.resistance_temp_dict["T"]<temperature)[0]
        if len(resistance_range_indices) == 0:
            print("ERROR: Requested resistance fit is not bounded by current table (input temperature too low)")
            print("Min T for table: " + str(self.resistance_temp_dict["T"][0]))
            print("Max T for table: " + str(self.resistance_temp_dict["T"][-1]))
            print("Returning min resistance available")
            return np.min(self.resistance_temp_dict["R"])
            return
        lower_temperature_index = resistance_range_indices[-1]
        temperatures_either_side = self.resistance_temp_dict["T"][lower_temperature_index:lower_temperature_index+2]
        resistances_either_side = self.resistance_temp_dict["R"][lower_temperature_index:lower_temperature_index+2]
        slope = (resistances_either_side[1] - resistances_either_side[0])/(temperatures_either_side[1] - temperatures_either_side[0])
        b = resistances_either_side[0] - (slope * temperatures_either_side[0])
        resistance_fit = slope*temperature + b
        return resistance_fit
