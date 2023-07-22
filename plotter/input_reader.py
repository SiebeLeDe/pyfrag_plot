import numpy as np
import os
from os.path import join as opj

# Local imports
from plotter.file_func import get_pyfrag_files


def create_plotpath(self, plotpath):
    """
    Takes as argument the desired plotpath for the plots
    If the directory does not exist, it creates one
    """
    self.path = plotpath
    if not os.path.isdir(self.path):
        os.mkdir(self.path)


def read_inputfile(self, inputfile):
    """
    Takes as argument the inputfile for the pyfrag calculation
    Extracts extra specifications such as orbitalenergy, overlap, population of a certain fragment and MO
    """
    self.special_keys = {}
    old_spec = ""
    spec_counter = 0
    with open(inputfile) as file:
        for line in file:
            elements = line.split(" ")
            for index, element in enumerate(elements):
                # Replace the frag1 and frag2 strings with the names of the fragments, which are seperated by an underscore
                if "frag1" in elements:
                    elements[elements.index("frag1")] = self.name.split("_")[0]
                if "frag2" in elements:
                    elements[elements.index("frag2")] = self.name.split("_")[1]
                # Checks if an element of a line is in the extra_keys list ...
                if element in ["orbitalenergy", "overlap", "population"]:
                    if old_spec in "":
                        old_spec = elements[0]
                    if elements[0] in old_spec:
                        spec_counter += 1
                    else:
                        spec_counter = 1
                    # ... if so, the dictionary 'special_keys' is appended with the special key
                    self.special_keys[f"{elements[0]}_{spec_counter}"] = {}
                    elements[-1] = elements[-1].rstrip("\n")
                    self.special_keys[f"{elements[0]}_{spec_counter}"] = elements[1:]
                    old_spec = elements[0]


def read_data(self, datafile: str):
    """
    Creates a dictionary with with the keys specifying which data it represents (EDA term, energy, etc.)
    Takes as argument the absolute path to the pyfrag output file
    """
    header = np.genfromtxt(datafile, max_rows=1, dtype=str, comments=None)  # type: ignore
    steps = np.genfromtxt(datafile, usecols=[0], dtype=int)
    data = np.genfromtxt(datafile, usecols=range(1, len(header)), dtype=float)

    data = self.remove_outliers(data)

    # Processes the data
    self.datadic = {}
    self.specialkeys = {}
    self.datadic[header[0][1:]] = steps
    for i, key in enumerate(header[1:]):
        # Replaces uninformative headers like 'orbitalenergy_1' with for example 'orbitalenergy_A_CGeP_33'
        if key in self.special_keys.keys():
            new_key = f'{key[:-1]}{"_".join(self.special_keys[key])}'
            self.datadic[new_key] = data[: self.max_steps + 1, i]
            # Keeps track which keys are changed
            if key[:3] not in self.specialkeys:
                self.specialkeys[key[:3]] = []
                self.specialkeys[key[:3]].append(new_key)
            else:
                self.specialkeys[key[:3]].append(new_key)
        else:
            self.datadic[key] = data[: self.max_steps + 1, i]
    # Makes a dictionary with the results at the peak (maximum of total energy/bond energy)
    self.peakdic = {}
    peakstep = self.determine_stationary_point(self.datadic["EnergyTotal"])
    for key, array in self.datadic.items():
        self.peakdic[key] = array[peakstep]

    # for key,value in self.specialkeys.items():
    #    print(key, value)

    # for key,value in self.peakdic.items():
    #    print(key, value)


def main():
    path_to_pyfrag_results = r"C:\Users\siebb\VU_PhD\PhD\Projects\Squaramides\pyfrag_results"
    system_name = "deltamides_di_O_Cs_all"

    pyfrag_result_files = get_pyfrag_files(opj(path_to_pyfrag_results, system_name))
    print(pyfrag_result_files)


if __name__ == "__main__":
    main()
