from typing import List, Optional
import numpy as np
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import os
import pyfrag_plotter as pfp
import plot_parameters as pp
from os.path import join as j


class SoloPlotter:
    def __init__(self, inputfile, resultfile, color, systemname):
        # Init variables
        self.name = systemname
        self.color = color

        # Init functions
        self.read_inputfile(inputfile)
        self.read_data(resultfile)
        self.check_disp_term()

    def plot(self, plotpath, plotparameter=False):
        # Plot functions
        if plotparameter:
            self.create_plotpath(plotpath)
            self.plot_eda_terms()
            self.plot_asm_terms()

            # Plotting "special keys" like overlap, orbitalenergies & gross populations
            # ove_key, pop_key, orb_key = self.check_terms()
            # if ove_key: self.plot_overlaps(self.specialkeys['ove'])
            # if pop_key: self.plot_populations(self.specialkeys['pop'])
            # if orb_key: self.plot_energygaps(self.specialkeys['orb'])

            print(f"Plots succesfully made for {self.name}")

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
                    if element in pfp.extra_keys:
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

        # Determines until which step the data should be processed (eventually plotted)
        self.max_steps = len(steps) - 1
        if isinstance(pfp.max_plotstep, int):
            self.max_steps = pfp.max_plotstep
        elif isinstance(pfp.max_plotstep, float):
            # First find to which array the specified bondlength should be compared to, for example a stretch coord of an angle
            try:
                irc_index = np.where(header == pfp.irc_coord)[0] - 1
            except IndexError:
                raise NameError(f"{pfp.irc_coord} not in header of pyfrag text file")
            # Then determine the nearest value using the correct array
            self.max_steps = np.abs(data[:, irc_index] - pfp.max_plotstep).argmin()
        elif isinstance(pfp.max_plotstep, str):
            self.max_steps = self.determine_stationary_point(data[:, 1])

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

    def remove_outliers(self, data_matrix):
        """
        Removes outliers in the data (caused by forcing restricted conditions)
        The threshold is specified in plot_parameters.py and the outlier is removed when
        its value is higher than the threshold compared to its neighboring values
        """
        axis = 1  # check the pyfrag txt file to see with column is the best option
        delete_counter = 0  # the array of which indices are deleted becomes shorter and thus a correction is needed

        for i in range(1, len(data_matrix[:, axis]) - 1):
            i -= delete_counter
            if (abs(data_matrix[i, axis] - data_matrix[i - 1, axis]) >= pp.outlier_threshold and abs(data_matrix[i, axis] - data_matrix[i + 1, axis]) >= pp.outlier_threshold):
                data_matrix = np.delete(data_matrix, i, 0)
                delete_counter += 1
        return data_matrix

    def check_disp_term(self):
        """
        Removes the dispersion term in the EDA if its contribution is 0 or near 0
        """
        self.EDA_keys = pp.EDA_keys
        self.EDA_names = pp.EDA_names
        if abs(np.sum(self.datadic[self.EDA_keys[-1]])) < 1.0:
            self.EDA_keys.remove(self.EDA_keys[-1])
            self.EDA_names.remove(self.EDA_names[-1])

    def check_terms(self):
        """
        Determines if overlaps, orbitalenergies and/or gross populations have been calculated
        """
        ove_key = False
        pop_key = False
        orb_key = False
        if "ove" in self.specialkeys:
            ove_key = True
        if "pop" in self.specialkeys:
            pop_key = True
        if "orb" in self.specialkeys:
            orb_key = True
        return ove_key, pop_key, orb_key

    def determine_stationary_point(self, energy_array):
        """
        Determines the step at which a stationary point is reached:
        either the minimum or maximum of the supplied energy array
        """
        if pp.stat_point.lower() == "min":
            return np.argmin(energy_array)
        if pp.stat_point.lower() == "max":
            return np.argmax(energy_array)
        else:
            raise ValueError("stat_point in plot_parameters.py should be either 'min' or 'max'")

    def get_energygap(self, f1, f2):
        """
        Determines the HOMO LUMO gap
        Takes two keys, present in the datadic, and determines the absolute difference
        """
        if "orbitalenergy" not in f1 and "orbitalenergy" not in f2:
            return print("Error HOMO-LUMO gap calculation")
        return np.abs(self.datadic[f1] - self.datadic[f2]) * pp.har_eV_ratio

    def get_stabilization(
        self,
        overlapkey,
        e_key1,
        e_key2,
    ):
        """
        Determines the stabilization S^2/gap for a certain MO pair
        Important: the MO pair in the overlapkey should correspond to the MO pair of the individual orbitalenergy keys
        Returns the stabilization in units [S^2 / eV]
        """
        gap = self.get_energygap(e_key1, e_key2)
        S = self.datadic[overlapkey]
        return np.square(S) / gap

    def get_peakinfo(self, dic=True):
        """
        Returns information on the peak step:
           dic = True: returns the dictionary containing all the results at the peak position
           dic = False: returns the step at which the energy peak as been reached
        """
        if dic:
            return self.peakdic
        else:
            return self.peakdic["IRC"] - 1

    def get_systeminfo(self):
        """
        Returns the name, dictrionary with the data, color and ... of the instance
        This method is used in the multiplot class
        """
        return self.name, self.datadic, self.color

    def get_specialkey(self, key: Optional[str] = None):
        """
        Returns a dictionary containing the data names of special keys such as 'overlap', 'orbitalenergy', etc.
        The user can choose which special key will be returned
        """
        if key:
            if key in "overlap" or key == "ove":
                return self.specialkeys["ove"]
            if key in "population" or key == "pop":
                return self.specialkeys["pop"]
            if key in "orbitalenergy" or key == "orb":
                return self.specialkeys["orb"]
        else:
            return self.specialkeys

    def get_eda_keys(self):
        """
        Returns a list containing the EDA keys. This method is necessary because the dispersion term could be removed for this instance
        This method is used in the multiplot class
        """
        return self.EDA_keys, self.EDA_names

    def plot_energygaps(self, orb_keys):
        """
        Takes as argument the keys which represent the data with the orbital energies
        Plots the specified energy gaps and saves the figure
        """
        for i in range(0, len(orb_keys), 2):
            MO_pair = ["_".join(orb_keys[i].split("_")[1:]), "_".join(orb_keys[i + 1].split("_")[1:])]
            label = "_".join(MO_pair)
            gap = self.get_energygap(orb_keys[i], orb_keys[i + 1])
            plt.plot(self.datadic[pfp.irc_coord], gap, label=label, color=pp.solo_col[i])
            set_plot_details(ylabel="\u03B5 / eV", title=f"Energy Gap #{i}", savefig=j(self.path, "Energy Gap #{i}.png"))

    def plot_populations(self, pop_keys):
        """
        Takes as argument the keys which represent the population of orbitals
        Plots the specified populations and saves the figure
        """
        color_counter = 0
        style_counter = 0
        for i, key in enumerate(pop_keys):
            if i % 2 == 0 and i != 0:
                color_counter += 1
            label = "_".join(key.split("_")[1:])
            plt.plot(self.datadic[pfp.irc_coord], self.datadic[key], label=label, color=pp.solo_col[color_counter], linestyle=pp.styles[style_counter])
            style_counter = switch(style_counter)
        set_plot_details(ylabel="Gross Population", title=f"Gross Populations of {self.name}", savefig=j(self.path, "GrossPopulations.png"), ylim=[0, 2],)

    def plot_overlaps(self, overlap_keys):
        """
        Takes as argument the keys which represent the overlap between two orbitals
        Plots the specified overlap(s) and saves the figure
        """
        for i, key in enumerate(overlap_keys):
            label = "_".join(key.split("_")[1:])
            plt.plot(
                self.datadic[pfp.irc_coord],
                self.datadic[key],
                label=label,
                color=pp.solo_col[i],
            )
        set_plot_details(
            ylabel="Overlap $\itS$",
            title=f"Overlaps of {self.name}",
            savefig=j(self.path, "Overlaps.png"),
            ylim=[0, 1],
        )

    def plot_eda_terms(self):
        """
        Plots the EDA terms in either a combined graph or in seperate graphs
        """
        for i, key in enumerate(self.EDA_keys):
            plt.plot(
                self.datadic[pfp.irc_coord],
                self.datadic[key],
                label=self.EDA_names[i],
                color=pp.solo_col[i],
            )
        set_plot_details(
            ylabel="\u0394$\it{E}$ / kcal mol$^{-1}$",
            title=f"EDA terms of {self.name}",
            savefig=j(self.path, "EDA.png"),
        )

    def plot_asm_terms(self):
        """
        Plots the ASM terms in a combined graph
        """
        for i, key in enumerate(pp.ASM_keys[:3]):
            plt.plot(
                self.datadic[pfp.irc_coord],
                self.datadic[key],
                label=pp.ASM_names[i],
                color=pp.solo_col[i],
            )
        set_plot_details(
            ylabel="\u0394$\it{E}$ / kcal mol$^{-1}$",
            title=f"ASM terms of {self.name}",
            savefig=j(self.path, "ASM.png"),
        )


class MultiPlotter:
    def __init__(self, plotpath, instances):
        self.instances = instances
        self.path = plotpath

    def plot(self, interpolate_coord: Optional[float] = None):
        """
        Plots graphs such as ASM, EDA, overlaps, populations etc. for all systems combined
        """
        disp, overlap, population, orbenergy = self.check_terms()

        if pp.vline and interpolate_coord:
            self.vline = float(interpolate_coord)
        else:
            self.vline = None

        self.plot_multiple_asm()
        self.plot_multiple_asm(plot_extra_strain=True)
        self.plot_multiple_eda(disp_check=disp)

        # if overlap:
        #     self.plot_multiple_overlap()
        # if population:
        #     self.plot_multiple_population()
        # if orbenergy:
        #     self.plot_multiple_energygap()
        # if orbenergy and population:
        #     self.plot_multiple_stabilization()
        print("Multi plots succesfully made\n")

    def check_terms(self):
        """
        Checks if certain keys/terms are present in the data and in EDA keys that should be plotted by returning True ('yes') or False ('no') for each
        """
        disp_check = False
        overlap_check = False
        population_check = False
        orbitalenergy_check = False
        for inst in self.instances:
            EDA_keys, _ = inst.get_eda_keys()
            special_keys = inst.get_specialkey()
            if "Disp" in EDA_keys:
                disp_check = True
            if "ove" in special_keys:
                overlap_check = True
            if "pop" in special_keys:
                population_check = True
            if "orb" in special_keys:
                orbitalenergy_check = True
        return disp_check, overlap_check, population_check, orbitalenergy_check

    def get_max_peaklength(self):
        """
        Checks which system has the highest peak and return the coordinate corresponding to that peak
        """
        peaks = [inst.get_peakinfo()[pfp.irc_coord] for inst in self.instances]
        return max(peaks)

    def plot_multiple_asm(self, plot_extra_strain=False):
        """
        Plots the ASM terms being Ebond, Eint and Estrain
        """
        plot_keys = pp.ASM_keys
        file_name = "ASM_Combined.png"

        if plot_extra_strain:
            plot_keys = pp.ASM_strain_keys
            file_name = "ASM_Strain.png"

        for i, key in enumerate(plot_keys):
            for system in self.instances:
                name, data, color = system.get_systeminfo()
                peakdic = system.get_peakinfo()
                if i == 0:
                    plt.plot(
                        data[pfp.irc_coord],
                        data[key],
                        label=name,
                        color=color,
                        linestyle=pp.ASM_styles[i],
                    )
                    plt.scatter(peakdic[pfp.irc_coord], peakdic[key], color=color, s=50)
                    continue

                plt.plot(
                    data[pfp.irc_coord],
                    data[key],
                    color=color,
                    linestyle=pp.ASM_styles[i],
                )
            if i == len(plot_keys)-1:
                set_plot_details(
                    ylabel="\u0394$\it{E}$ / kcal mol$^{-1}$",
                    title="ASM Analysis",
                    vline=self.vline,
                    ylim=pp.ASM_ylim,
                    savefig=j(self.path, file_name),
                    zero_line=True,
                )

    def plot_multiple_eda(self, disp_check):
        """
        Plots the EDA terms for each instance in one graph and in seperate graphs
        """
        # Combined graph
        for system in self.instances:
            name, data, color = system.get_systeminfo()
            EDA_keys, _ = system.get_eda_keys()
            peakdic = system.get_peakinfo()
            for i, key in enumerate(EDA_keys):
                if i == 0:
                    plt.plot(
                        data[pfp.irc_coord],
                        data[key],
                        label=name,
                        color=color,
                        linestyle=pp.EDA_styles[i],
                    )
                    plt.scatter(peakdic[pfp.irc_coord], peakdic[key], color=color, s=50)
                else:
                    plt.plot(
                        data[pfp.irc_coord],
                        data[key],
                        color=color,
                        linestyle=pp.EDA_styles[i],
                    )
        set_plot_details(
            ylabel="\u0394$\it{E}$ / kcal mol$^{-1}$",
            title="EDA Analysis",
            vline=self.vline,
            zero_line=True,
            savefig=j(self.path, "EDA_Combined.png"),
            ylim=pp.EDA_ylim,
        )

        # Seperated graph for each term
        if disp_check:
            EDA_keys, EDA_names = pp.EDA_keys, pp.EDA_names
        else:
            EDA_keys, EDA_names = self.instances[0].get_eda_keys()

        for i, key in enumerate(EDA_keys):
            for system in self.instances:
                name, data, color = system.get_systeminfo()
                peakdic = system.get_peakinfo()
                plt.plot(data[pfp.irc_coord], data[key], label=name, color=color)
                plt.scatter(peakdic[pfp.irc_coord], peakdic[key], color=color, s=50)
            set_plot_details(
                ylabel="\u0394$\it{E}$ / kcal mol$^{-1}$",
                title=f"EDA term {EDA_names[i]}",
                vline=self.vline,
                zero_line=True,
                savefig=j(self.path, f"EDA_{EDA_names[i]}.png"),
            )

    def plot_multiple_overlap(self):
        """
        Plots the overlap for each instance for the same MO pair in seperate graphs
        Note: it assumes that the number of MO pairs is the same for each instance
        """
        overlap_keys = [system.get_specialkey("ove") for system in self.instances]
        for i in range(len(overlap_keys[0])):
            for k, system in enumerate(self.instances):
                _, data, color = system.get_systeminfo()
                peakdic = system.get_peakinfo()
                label = "_".join(overlap_keys[k][i].split("_")[1:])
                plt.plot(
                    data[pfp.irc_coord],
                    data[overlap_keys[k][i]],
                    label=label,
                    color=color,
                )
                plt.scatter(
                    peakdic[pfp.irc_coord], peakdic[overlap_keys[k][i]], color=color
                )
            set_plot_details(
                ylabel="Overlap $\itS$",
                title="Overlap",
                savefig=j(self.path, f"Overlap_{i}.png"),
                ylim=[0, 1],
            )

    def plot_multiple_population(self):
        """
        Plots the gross populations for each instance for the same MO pair in seperate graphs
        Note: it assumes that the number of MO pairs is the same for each instance
        """
        population_keys = [system.get_specialkey("pop") for system in self.instances]
        for i in range(0, len(population_keys[0]), 2):
            for k, system in enumerate(self.instances):
                _, data, color = system.get_systeminfo()
                peakdic = system.get_peakinfo()
                labels = [
                    "_".join(population_keys[k][i].split("_")[1:]),
                    "_".join(population_keys[k][i + 1].split("_")[1:]),
                ]
                plt.plot(
                    data[pfp.irc_coord],
                    data[population_keys[k][i]],
                    label=labels[0],
                    color=color,
                    linestyle=pp.styles[0],
                )
                plt.plot(
                    data[pfp.irc_coord],
                    data[population_keys[k][i + 1]],
                    label=labels[1],
                    color=color,
                    linestyle=pp.styles[1],
                )
                plt.scatter(
                    peakdic[pfp.irc_coord], peakdic[population_keys[k][i]], color=color
                )
                plt.scatter(
                    peakdic[pfp.irc_coord],
                    peakdic[population_keys[k][i + 1]],
                    color=color,
                )
            set_plot_details(
                ylabel="Gross Population",
                title="Gross populations",
                savefig=j(self.path, f"Population_{i}.png"),
                ylim=[0, 2],
            )

    def plot_multiple_energygap(self):
        """
        Plots the energy gap for each instance for the same MO pair in seperate graphs
        Note: it assumes that the number of MO pairs is the same for each instance
        """
        energy_keys = [system.get_specialkey("orb") for system in self.instances]
        for i in range(0, len(energy_keys[0]), 2):
            for k, system in enumerate(self.instances):
                _, data, color = system.get_systeminfo()
                peakdic = system.get_peakinfo()
                gap = system.get_energygap(energy_keys[k][i], energy_keys[k][i + 1])
                MO_pair = [
                    "_".join(energy_keys[k][i].split("_")[1:]),
                    "_".join(energy_keys[k][i + 1].split("_")[1:]),
                ]
                plt.plot(data[pfp.irc_coord], gap, label="_".join(MO_pair), color=color)
                plt.scatter(
                    peakdic[pfp.irc_coord], gap[peakdic["IRC"] - 1], color=color
                )
            set_plot_details(
                ylabel="\u03B5 / eV",
                title="Energy gaps",
                savefig=j(self.path, f"EnergyGap_{i}.png"),
            )

    def plot_multiple_stabilization(self):
        """
        Plots the stabilization (S^2/gap) of a certain MOpair for each instance
        Note: it assumes that the number of MO pairs is the same for each instance and that the overlapkey represent the same
        MO pair as the orbital energy keys
        """
        energy_keys = [system.get_specialkey("orb") for system in self.instances]
        overlap_keys = [system.get_specialkey("ove") for system in self.instances]
        e_counter = 0
        for i in range(0, len(energy_keys[0]) // 2):
            for k, system in enumerate(self.instances):
                _, data, color = system.get_systeminfo()
                peakdic = system.get_peakinfo()
                stabilization = system.get_stabilization(
                    overlap_keys[k][i],
                    energy_keys[k][e_counter],
                    energy_keys[k][e_counter + 1],
                )
                MOpair = "_".join(overlap_keys[k][i].split("_")[1:])
                plt.plot(data[pfp.irc_coord], stabilization, label=MOpair, color=color)
                plt.scatter(
                    peakdic[pfp.irc_coord],
                    stabilization[peakdic["IRC"] - 1],
                    color=color,
                )
            set_plot_details(
                ylabel="$\itS$² / \u03B5",
                title="Stabilizations",
                savefig=j(self.path, f"Stabilization_{i}.png"),
            )
            e_counter += 2


# ################# Functions ###################

def switch(value):
    """
    Acts as a switch by returning 1 when the value is 0 and vice versa
    """
    if value == 1:
        return 0
    else:
        return 1


def set_plot_details(
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    title: Optional[str] = None,
    savefig: Optional[str] = None,
    clear: Optional[bool] = True,
    ylim: Optional[List[float]] = None,
    vline: Optional[float] = None,
    zero_line: Optional[bool] = None,
):
    """
    Function that specifies plot options for making a shorter and cleaner code
    """
    ax = plt.gca()

    # Plot labels
    if xlabel:
        plt.xlabel(xlabel, labelpad=20)
    else:
        plt.xlabel(f"{pfp.irc_coords[pfp.irc_coord]} / \u00c5")

    if ylabel:
        plt.ylabel(ylabel, labelpad=20)

    # Specfies the y limits
    if ylim:
        plt.ylim(ylim[0], ylim[1])

    # Plot x limits
    plt.xlim(pp.xlim[0], pp.xlim[1])

    # Reverses the plot direction by reversing the x-axis
    if pfp.irc_coord == "bondlength_2":
        ax.set_xlim(ax.get_xlim()[::-1])

    # Draws a vertical line at the specified point
    if vline:
        print(pp.vline)
        plt.vlines(
            vline,
            ax.get_ylim()[0],
            ax.get_ylim()[1],
            colors=["grey"],
            linestyles="dashed",
        )

    # Draws a horizontal line at y=0 (indicating the 'zero line')
    if True:
        plt.hlines(0, ax.get_xlim()[0], ax.get_xlim()[1], colors=["grey"], linewidth=0.2)

    # Axes adjustments: tick markers and number of ticks
    ax.tick_params(which="both", width=2)
    ax.tick_params(which="major", length=7)
    ax.xaxis.set_major_locator(MaxNLocator(5))
    ax.yaxis.set_major_locator(MaxNLocator(5))

    # Removes the top en right border of the graph
    right_side = ax.spines["top"]
    top_side = ax.spines["right"]
    right_side.set_visible(False)
    top_side.set_visible(False)

    # Makes the x and y axis wider
    ax.spines["left"].set_linewidth(2)
    ax.spines["bottom"].set_linewidth(2)

    # Fixes the large padding between the axes and the labels of the axes
    plt.tight_layout()

    # Adds more spacing between ticks and the labels
    ax.tick_params(pad=10)

    # Plots the legend at the right side of the plot
    # ax.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", mode="expand")
    ax.legend(frameon=False)

    # Plots the title
    # plt.title(title,pad=10)

    # Saves the figure in standard .png format.
    plt.savefig(savefig, dpi=250)

    # Clears the plot if specified
    if clear:
        plt.clf()
