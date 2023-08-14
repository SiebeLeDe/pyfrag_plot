# Code that contains a class/function used for interpolating data from the PyFrag calculations
# Siebe Lekanne Deprez | 4 Feb 2022
from typing import Dict
import pyfrag_plotter.main as pfp
import plot_parameters as pp
import numpy as np
from os.path import join as j
# from attr import dataclass

all_keys = [
    "EnergyTotal",
    "Int",
    "StrainTotal",
    "frag1Strain",
    "frag2Strain",
    "Int",
    "Elstat",
    "OI",
    "Pauli",
]
ASM_keys = ["EnergyTotal", "Int", "StrainTotal"]
Strain_keys = ["StrainTotal", "frag1Strain", "frag2Strain"]
EDA_keys = ["Int", "Elstat", "OI", "Pauli"]  # 'Disp'
MO_terms = []

# ################# Class ###################


# @dataclass
# class SystemInterpolationStorage:
#     name: str


class InterpolatePyFragData:
    """
    Class that interpolates data from PyFrag results.
    The user should specify the desired bondlength at which the data is interpolated
    and the user should give as argument the *SoloPlotter* instances created in the PyFragPlotter.py file
    """

    def __init__(self, instances, bondlength):
        self.systems = instances
        self.bondlength = bondlength
        self.interpol_indices = []
        self.interpolated_data: Dict[str, Dict[str, float]] = {}
        self.interpolated_specialkeys: Dict[str, Dict[str, Dict[str, Dict[str, float]]]] = {}

    def interpolate(self):
        """
        The main loop for calculating the interpolated data at the desired bondlength for each system
        Makes a dictionary with the format: name (string) | interpolated data (array)
        """
        self.interpolated_specialkeys = {}
        self.max_n = 0  # Used in specifying the number of special keys for each system
        for system in self.systems:
            name, data, _ = system.get_systeminfo()
            i_points, x_points = self.determine_nearest_twopoints(data)
            self.interpolated_data[name] = self.interpolate_keys(i_points, x_points, data)
            self.interpolated_specialkeys[name] = self.interpolate_specialkeys(i_points, x_points, system, data)
            self.interpol_indices.append(i_points)

    def determine_nearest_twopoints(self, data):
        """
        Determines which indices in the bondlength array are the closest to the desired bondlength
        Then it uses the indices to interpolate data at the desired bondlength
        Returns Dictionary with the format: keys | y-values of one key for each key
        """
        diff_array = data[pfp.irc_coord] - self.bondlength

        if self.bondlength <= np.min(data[pfp.irc_coord]) or self.bondlength >= np.max(data[pfp.irc_coord]):
            raise ValueError("""
                            Desired bondlength out of range\n
                            Check if the max_plotstep does not limit the desired bondlength\n""")

        # Checks where the sign changes (i.e. closest values from above and beneath the
        # specified bondlength)
        init_sign = np.sign(diff_array[0])
        flip_index = 0
        for index, value in enumerate(diff_array):
            if init_sign != np.sign(value):
                flip_index = index
                break

        i_interpol = [flip_index - 1, flip_index]
        nearest_points = [data[pfp.irc_coord][i_interpol[0]], data[pfp.irc_coord][i_interpol[1]]]

        return i_interpol, nearest_points

    def interpolate_keys(self, i_points, x_points, data) -> Dict[str, float]:
        """
        Calculates the interpolated data using the indices (i_points) and nearest x-values (x_points) around the desired bondlength
        Returns Dictionary with the format: keys | y-values of one key for each key
        """
        # Uses the nearest points to solve a linear equation for specific data,
        # specified by the keys in the inter_keys1 list
        ret_data = {}
        for key in all_keys:
            y_points = [data[key][i_points[0]], data[key][i_points[1]]]
            ret_data[key] = self.solve_linear_equation(x_points, y_points)
        return ret_data

    def interpolate_specialkeys(self, i_points, x_points, system, systemdata):
        """
        Interpolated data of special keys using the indices (i_points) and nearest x-values (x_points) around the desired bondlength
        Returns Dictionary with the format: keys | y-values of one key for each key
        """
        specialkeys_dic = system.get_specialkey()
        ret_data = {}
        len_ove_inputs = 0
        len_orb_inputs = 0
        len_pop_inputs = 0

        ove_key, pop_key, orb_key = system.check_terms()

        if ove_key:
            len_ove_inputs = len(specialkeys_dic["ove"])
        if orb_key:
            len_orb_inputs = len(specialkeys_dic["orb"])
        if pop_key:
            len_pop_inputs = len(specialkeys_dic["pop"])

        n = 0
        # Assumes that for each overlap pair, the orbital energies and populations have also been calculated
        while n < max([len_ove_inputs, len_orb_inputs // 2, len_pop_inputs // 2]):
            ret_data[f"#{n}"] = {}

            if n <= len_ove_inputs:
                key = list(specialkeys_dic["ove"])[n]
                MO_pair = "_".join(key.split("_")[1:])
                y_points = [systemdata[key][i_points[0]], systemdata[key][i_points[1]]]
                interpol_data = self.solve_linear_equation(x_points, y_points)

                ret_data[f"#{n}"]["ove"] = {}
                ret_data[f"#{n}"]["ove"]["pair"] = MO_pair
                ret_data[f"#{n}"]["ove"]["data"] = interpol_data

            if n * 2 + 1 <= len_orb_inputs:
                keys = [list(specialkeys_dic["orb"])[2 * n], list(specialkeys_dic["orb"])[2 * n + 1]]
                MO_pair = ["_".join(keys[0].split("_")[1:]), "_".join(keys[1].split("_")[1:])]
                gap = system.get_energygap(keys[0], keys[1])

                # y_points of the energy gap
                y_points_gap = [gap[i_points[0]], gap[i_points[1]]]
                interpol_gapdata = self.solve_linear_equation(x_points, y_points_gap)

                # y_points of the first MO of the pair
                y_points_1 = [systemdata[keys[0]][i_points[0]], systemdata[keys[0]][i_points[1]]]
                interpol_MO1data = self.solve_linear_equation(x_points, y_points_1)

                # y_points of the second MO of the pair
                y_points_2 = [systemdata[keys[1]][i_points[0]], systemdata[keys[1]][i_points[1]]]
                interpol_MO2data = self.solve_linear_equation(x_points, y_points_2)

                ret_data[f"#{n}"]["orb"] = {}
                ret_data[f"#{n}"]["orb"]["pair"] = MO_pair
                ret_data[f"#{n}"]["orb"]["data"] = interpol_gapdata
                ret_data[f"#{n}"]["orb"]["MO1"] = interpol_MO1data * pp.har_eV_ratio
                ret_data[f"#{n}"]["orb"]["MO2"] = interpol_MO2data * pp.har_eV_ratio

            if n * 2 + 1 <= len_pop_inputs:
                keys = [list(specialkeys_dic["pop"])[2 * n], list(specialkeys_dic["pop"])[2 * n + 1]]
                MO_pair = ["_".join(keys[0].split("_")[1:]), "_".join(keys[1].split("_")[1:])]

                # Interpolates the data of the first MO in the MOpair
                y_points1 = [systemdata[keys[0]][i_points[0]], systemdata[keys[0]][i_points[1]]]
                interpol_data1 = self.solve_linear_equation(x_points, y_points1)

                # Interpolates the data of the second MO in the MOpair
                y_points2 = [systemdata[keys[1]][i_points[0]], systemdata[keys[1]][i_points[1]]]
                interpol_data2 = self.solve_linear_equation(x_points, y_points2)

                ret_data[f"#{n}"]["pop"] = {}
                ret_data[f"#{n}"]["pop"]["pair"] = MO_pair
                ret_data[f"#{n}"]["pop"]["data"] = [interpol_data1, interpol_data2]
            n += 1
        if n >= self.max_n:
            self.max_n = n

        # for n in ret_data:
        #     print(n)
        #     for key in ret_data[n]:
        #         print('\t',key)
        #         for secondkey in ret_data[n][key]:
        #             print('\t\t',ret_data[n][key][secondkey])

        return ret_data

    def solve_linear_equation(self, x_points, y_points):
        """
        Finds the values for a and b in the equation y=ax+b
        Returns the interpolated value (y-coordinate)
        """
        a = (y_points[1] - y_points[0]) / (x_points[1] - x_points[0])  # a = (y2-y1)/(x2-x1)
        b = y_points[0] - a * x_points[0]                              # b = y1-a*x1 (or equivalently: b = y2-a*x2)
        return a * self.bondlength + b

    def print_interpolated_data(self, folder):
        """
        Prints the interpolated data in a table format
        Note that the number of printing keys should be changed MANUALLY
        """
        with open(j(folder, "result.txt"), "a", encoding="utf-8") as outfile:
            outfile.write(f'{"-"*10} Interpolation at {self.bondlength :.2f} A {"-"*10}\n')
            outfile.write("System,index,coord1,coord2\n")
            for i, system in enumerate(self.systems):
                name, data, _ = system.get_systeminfo()
                new_indices = [[i + 1 for i in indexpair] for indexpair in self.interpol_indices]
                outfile.write(f"{name},[{new_indices[i][0]} {new_indices[i][1]}],{data[pfp.irc_coord][self.interpol_indices[i][0]] :.3f},{data[pfp.irc_coord][self.interpol_indices[i][1]]:.3f}\n")
            outfile.write("\n")

            outfile.write("ASM\n")
            outfile.write(f"System,{ASM_keys[0]},{ASM_keys[1]},{ASM_keys[2]}\n")
            for systemname, data in self.interpolated_data.items():
                outfile.write(f"{systemname},{data[ASM_keys[0]] :.2f},{data[ASM_keys[1]]:.2f},{data[ASM_keys[2]]:.2f}\n")
            outfile.write("\n")

            outfile.write("Extra Strain Decomposition\n")
            outfile.write(f"System,{Strain_keys[0]},{Strain_keys[1]},{Strain_keys[2]}\n")
            for systemname, data in self.interpolated_data.items():
                outfile.write(f"{systemname},{data[Strain_keys[0]] :.2f},{data[Strain_keys[1]]:.2f},{data[Strain_keys[2]]:.2f}\n")
            outfile.write("\n")

            outfile.write("EDA\n")
            outfile.write(f"System,{EDA_keys[0]},{EDA_keys[1]},{EDA_keys[2]},{EDA_keys[3]}\n")
            for systemname, data in self.interpolated_data.items():
                outfile.write(f"{systemname},{data[EDA_keys[0]] :.2f},{data[EDA_keys[1]]:.2f},{data[EDA_keys[2]]:.2f},{data[EDA_keys[3]]:.2f}\n")
            outfile.write("\n")

            outfile.write("Orbital Analysis\n")
            for i in range(0, self.max_n):
                if MO_terms and i < len(MO_terms):
                    outfile.write(f"#{i}: {MO_terms[i]} \n")
                else:
                    outfile.write(f"#{i}\n")

                # Write the orbital analysis to a file
                outfile.write("System, MO pair, Gross pop (electrons), E MO1 (eV), E MO2 (eV), Energy gap (eV), Overlap (au), Stabilization [S²/\u03B5 x 100] (1/eV) \n")
                for systemname, dic in self.interpolated_specialkeys.items():
                    try:
                        pair = " & ".join(dic[f"#{i}"]["orb"]["pair"])  # type: ignore since I apply not consistent typing in this script
                    except KeyError:
                        try:
                            pair = dic[f"#{i}"]["ove"]["pair"]
                        except KeyError:
                            pair = "Not present"

                    try:
                        pop = dic[f"#{i}"]["pop"]["data"]
                        pop = [f"{value :.2f}" for value in pop]  # type: ignore since I apply not consistent typing in this script
                    except KeyError:
                        pop = [0, 0]

                    try:
                        e_MO1 = dic[f"#{i}"]["orb"]["MO1"]
                    except KeyError:
                        e_MO1 = 0.0

                    try:
                        e_MO2 = dic[f"#{i}"]["orb"]["MO2"]
                    except KeyError:
                        e_MO2 = 0.0

                    try:
                        overlap = dic[f"#{i}"]["ove"]["data"]
                    except KeyError:
                        overlap = 0.0

                    try:
                        gap = dic[f"#{i}"]["orb"]["data"]
                    except KeyError:
                        gap = 0.0

                    if abs(gap) > 1e-8:
                        stabilization = overlap**2 / gap * 100
                    else:
                        stabilization = 0.0

                    # if MO_terms and i < len(MO_terms):
                    #     print(f"Interpolation Printing Exception: no MO pair is present for system {systemname} and step {i} {MO_terms[i]}")
                    # else:
                    #     print(f"Interpolation Printing Exception: no MO pair is present for system {systemname} and step {i}")

                    outfile.write(f"{systemname},{pair},{pop[0]} {pop[1]},{e_MO1 :.2f},{e_MO2 :.2f},{gap :.2f},{overlap :.3e},{stabilization :.4f}\n")
                outfile.write("\n")
