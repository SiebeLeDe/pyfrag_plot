import os
from os.path import join as j

from typing import List, Dict
import pyfrag_plotter.interpolate.interpolate as ip
import numpy as np
import plot_parameters as pp
from pyfrag_plotter.plot.plot_classes import MultiPlotter, SoloPlotter

np.set_printoptions(precision=2)

plot_systems_dic: Dict[str, Dict[str, List[str]]] = {
    "orbs": {
        "plot_all_O_di_ureas": ["ureas_di_O_Cs_all", "ureas_di_O_Cs_sigma", "ureas_di_O_Cs_pi"],
        # "plot_all_S_di_ureas": ["ureas_di_S_Cs_all", "ureas_di_S_Cs_sigma", "ureas_di_S_Cs_pi"],
        # "plot_all_Se_di_ureas": ["ureas_di_Se_Cs_all", "ureas_di_Se_Cs_sigma", "ureas_di_Se_Cs_pi"],
        # "plot_all_O_di_deltamides": ["deltamides_di_O_Cs_all", "deltamides_di_O_Cs_sigma", "deltamides_di_O_Cs_pi"],
        # "plot_all_S_di_deltamides": ["deltamides_di_S_Cs_all", "deltamides_di_S_Cs_sigma", "deltamides_di_S_Cs_pi"],
        # "plot_all_Se_di_deltamides": ["deltamides_di_Se_Cs_all", "deltamides_di_Se_Cs_sigma", "deltamides_di_Se_Cs_pi"],
        # "plot_all_O_di_squaramides": ["squaramides_di_O_Cs_all", "squaramides_di_O_Cs_sigma", "squaramides_di_O_Cs_pi"],
        # "plot_all_S_di_squaramides": ["squaramides_di_S_Cs_all", "squaramides_di_S_Cs_sigma", "squaramides_di_S_Cs_pi"],
        # "plot_all_Se_di_squaramides": ["squaramides_di_Se_Cs_all", "squaramides_di_Se_Cs_sigma", "squaramides_di_Se_Cs_pi"],
        # "plot_all_O_tri_ureas": ["ureas_tri_O_Cs_all", "ureas_tri_O_Cs_sigma", "ureas_tri_O_Cs_pi"],
        # "plot_all_S_tri_ureas": ["ureas_tri_S_Cs_all", "ureas_tri_S_Cs_sigma", "ureas_tri_S_Cs_pi"],
        # "plot_all_Se_tri_ureas": ["ureas_tri_Se_Cs_all", "ureas_tri_Se_Cs_sigma", "ureas_tri_Se_Cs_pi"],
        # "plot_all_O_tri_deltamides": ["deltamides_tri_O_Cs_all", "deltamides_tri_O_Cs_sigma", "deltamides_tri_O_Cs_pi"],
        # "plot_all_S_tri_deltamides": ["deltamides_tri_S_Cs_all", "deltamides_tri_S_Cs_sigma", "deltamides_tri_S_Cs_pi"],
        # "plot_all_Se_tri_deltamides": ["deltamides_tri_Se_Cs_all", "deltamides_tri_Se_Cs_sigma", "deltamides_tri_Se_Cs_pi"],
        # "plot_all_O_tri_squaramides": ["squaramides_tri_O_Cs_all", "squaramides_tri_O_Cs_sigma", "squaramides_tri_O_Cs_pi"],
        # "plot_all_S_tri_squaramides": ["squaramides_tri_S_Cs_all", "squaramides_tri_S_Cs_sigma", "squaramides_tri_S_Cs_pi"],
        # "plot_all_Se_tri_squaramides": ["squaramides_tri_Se_Cs_all", "squaramides_tri_Se_Cs_sigma", "squaramides_tri_Se_Cs_pi"],
    },
    # "chalcs": {
    #     "plot_all_OSSe_di_ureas": ["ureas_di_O_Cs_all", "ureas_di_S_Cs_all", "ureas_di_Se_Cs_all"],
    #     "plot_pi_OSSe_di_ureas": ["ureas_di_O_Cs_pi", "ureas_di_S_Cs_pi", "ureas_di_Se_Cs_pi"],
    #     "plot_sigma_OSSe_di_ureas": ["ureas_di_O_Cs_sigma", "ureas_di_S_Cs_sigma", "ureas_di_Se_Cs_sigma"],
    #     "plot_all_OSSe_di_deltamides": ["deltamides_di_O_Cs_all", "deltamides_di_S_Cs_all", "deltamides_di_Se_Cs_all"],
    #     "plot_pi_OSSe_di_deltamides": ["deltamides_di_O_Cs_pi", "deltamides_di_S_Cs_pi", "deltamides_di_Se_Cs_pi"],
    #     "plot_sigma_OSSe_di_deltamides": ["deltamides_di_O_Cs_sigma", "deltamides_di_S_Cs_sigma", "deltamides_di_Se_Cs_sigma"],
    #     "plot_all_OSSe_di_squaramides": ["squaramides_di_O_Cs_all", "squaramides_di_S_Cs_all", "squaramides_di_Se_Cs_all"],
    #     "plot_pi_OSSe_di_squaramides": ["squaramides_di_O_Cs_pi", "squaramides_di_S_Cs_pi", "squaramides_di_Se_Cs_pi"],
    #     "plot_sigma_OSSe_di_squaramides": ["squaramides_di_O_Cs_sigma", "squaramides_di_S_Cs_sigma", "squaramides_di_Se_Cs_sigma"],
    #     "plot_all_OSSe_tri_ureas": ["ureas_tri_O_Cs_all", "ureas_tri_S_Cs_all", "ureas_tri_Se_Cs_all"],
    #     "plot_pi_OSSe_tri_ureas": ["ureas_tri_O_Cs_pi", "ureas_tri_S_Cs_pi", "ureas_tri_Se_Cs_pi"],
    #     "plot_sigma_OSSe_tri_ureas": ["ureas_tri_O_Cs_sigma", "ureas_tri_S_Cs_sigma", "ureas_tri_Se_Cs_sigma"],
    #     "plot_all_OSSe_tri_deltamides": ["deltamides_tri_O_Cs_all", "deltamides_tri_S_Cs_all", "deltamides_tri_Se_Cs_all"],
    #     "plot_pi_OSSe_tri_deltamides": ["deltamides_tri_O_Cs_pi", "deltamides_tri_S_Cs_pi", "deltamides_tri_Se_Cs_pi"],
    #     "plot_sigma_OSSe_tri_deltamides": ["deltamides_tri_O_Cs_sigma", "deltamides_tri_S_Cs_sigma", "deltamides_tri_Se_Cs_sigma"],
    #     "plot_all_OSSe_tri_squaramides": ["squaramides_tri_O_Cs_all", "squaramides_tri_S_Cs_all", "squaramides_tri_Se_Cs_all"],
    #     "plot_pi_OSSe_tri_squaramides": ["squaramides_tri_O_Cs_pi", "squaramides_tri_S_Cs_pi", "squaramides_tri_Se_Cs_pi"],
    #     "plot_sigma_OSSe_tri_squaramides": ["squaramides_tri_O_Cs_sigma", "squaramides_tri_S_Cs_sigma", "squaramides_tri_Se_Cs_sigma"],
    # }
}

# ################# General Data ###################
output_dir = "/Users/siebeld/Library/CloudStorage/OneDrive-VrijeUniversiteitAmsterdam/PhD/Projects/Squaramides/Plots"
pyfragresults_dir = "/Users/siebeld/Library/CloudStorage/OneDrive-VrijeUniversiteitAmsterdam/PhD/Projects/Squaramides/pyfrag_results"
# plot_type = 'Sync'#  'NP_trends' , 'E_trends'
# plotfoldername = 'AB_Test'# 'PlotFull_Ge_PSync_Ethy_Series'

# systems = ['CGeN_Ethy','SyncCGeN_Ethy'] # ['CSiN_Ethy','CGeN_Ethy','CSnN_Ethy'] # ['CGeN_Ethy','SyncCGeN_Ethy']# ['CSiN_Ethy','SyncCSiN_Ethy']
irc_coord = "bondlength"  # should correspond with the term in the pyfrag.txt file and it is shared across the whole file!
max_plotstep = None  # "peak"  # int value (index), float value (coord), 'peak', or None

solo_plot = False
multi_plot = True
irc_coords = {"bondlength": "r - r$_{eq}$"}
interpolate_option = 0.000   # string ("min" or "max" of total energy) or float 1.67 (coordinate in Angstrom)

# ################# Running ###################
if __name__ == "__main__":
    # Initializes the plot parameters
    pp.initialize_plot_parameters()
    for plot_type in plot_systems_dic.keys():
        # Checks whether the folder for the desired plottype (arbitrary category for organizing data) exists
        if not os.path.isdir(j(output_dir, plot_type)):
            os.mkdir(j(output_dir, plot_type))

        for plotfoldername, systems in plot_systems_dic[plot_type].items():
            # Checks whether the desired plotfolder exists
            if not os.path.isdir(j(output_dir, plot_type, plotfoldername)):
                os.mkdir(j(output_dir, plot_type, plotfoldername))

            print("Making new plot for systems: ", " ".join(systems))
            # Extract all the result files of the pyfrag calculations AND the corresponding input files where the printing keys like overlap are specified
            inputfiles = []
            resultfiles = []
            for counter, system in enumerate(systems):
                for file in os.listdir(j(pyfragresults_dir, system)):
                    if file.endswith(".in"):
                        inputfiles.append(j(pyfragresults_dir, system, file))
                    if file[:6] in "pyfrag_" and file.endswith(".txt"):
                        resultfiles.append(j(pyfragresults_dir, system, file))

            # Initiates the SoloPlotter class for each system in systems
            instances = []
            colors = pp.colors[plot_type]  # different types of plots have different color schemes

            for i, system in enumerate(systems):
                plotpath = j(output_dir, plot_type, plotfoldername, system)
                instances.append(SoloPlotter(inputfiles[i], resultfiles[i], colors[i], system, (irc_coord, irc_coords), max_plotstep))
                [inst.plot(plotpath, solo_plot) for inst in instances]

            # Initialises the plots with multiple systems
            multi_instance = MultiPlotter(j(output_dir, plot_type, plotfoldername), instances, (irc_coord, irc_coords))

            interpolate_dist = 0.0
            inst_interpolation = None
            if interpolate_option is not None:
                if isinstance(interpolate_option, str):
                    interpolate_dist = multi_instance.get_max_peaklength() + 0.00001
                    # Plots the PyFrag results. Useful for comparing results and trends of ASM, EDA and other points of interest
                    if multi_plot:
                        multi_instance.plot(interpolate_dist)
                else:
                    interpolate_dist = interpolate_option
                    multi_instance.plot(interpolate_dist)

                print(f"Interpolating at {interpolate_dist :.3f}")
                # Interpolates data at a specified bondlength (linear approximation)
                inst_interpolation = ip.InterpolatePyFragData(instances, interpolate_dist)
                inst_interpolation.interpolate()
            else:
                multi_instance.plot()

            # ################# Printing ###################
            print("-" * 10, " Settings ", "-" * 10)
            print(f"Solo plot           {solo_plot}")
            print(f"Multi plot          {multi_plot}")
            if interpolate_option is not None:
                print(f"Interpolate         {interpolate_dist :.3f}")
            print(f"Reaction coordinate {irc_coords[irc_coord]}")
            print(f"Output folder       {j(output_dir, plot_type, plotfoldername)}\n")

            print("-" * 10, " Peak Info ", "-" * 10)
            print()
            for system, inst in zip(systems, instances):
                print(f"{system} with {pp.stat_point} energy at {inst.get_peakinfo()['IRC'] :<3d}", end=" ")
                print(f"at coord = {inst.get_peakinfo()[irc_coord] :.4f} A", end=" ")
                print(f"with energy {inst.get_peakinfo()['EnergyTotal'] :.1f}")
            print()

            print("-" * 10, " Locations of inputfiles ", "-" * 10)
            [print(inputfile) for inputfile in inputfiles]
            print("")

            print("-" * 10, " Locations of resultfiles ", "-" * 10)
            [print(resultfile) for resultfile in resultfiles]
            print("")

            # Does the same as the previous printing block, but now writing it to a file
            with open(j(output_dir, plot_type, plotfoldername, "result.txt"), "w", encoding="utf-8") as outfile:

                outfile.write(f'{"-"*10} Settings {"-"*10}\n')
                outfile.write(f"Solo plot           {solo_plot}\n")
                outfile.write(f"Multi plot          {multi_plot}\n")
                if interpolate_option is not None:
                    outfile.write(f"Interpolate         {interpolate_dist :.3f}\n")
                outfile.write(f"Reaction coordinate {irc_coords[irc_coord]}\n")
                outfile.write(f"Output folder       {j(output_dir,plotfoldername)}\n")
                outfile.write("\n")

                outfile.write(f'{"-"*10} Peak Info {"-"*10}\n')
                for system, inst in zip(systems, instances):
                    outfile.write(f"{system} with {pp.stat_point} energy at {inst.get_peakinfo()['IRC'] :<3d}")
                    outfile.write(f"at coord = {inst.get_peakinfo()[irc_coord] :.4f} A")
                    outfile.write(f"with energy {inst.get_peakinfo()['EnergyTotal'] :.1f}\n")
                outfile.write("\n")

                outfile.write(f'{"-"*10} Locations of inputfiles {"-"*10}\n')
                [outfile.write(f"{inputfile}\n") for inputfile in inputfiles]
                outfile.write("\n")

                outfile.write(f'{"-"*10} Locations of resultfiles {"-"*10}\n')
                [outfile.write(f"{resultfile}\n") for resultfile in resultfiles]
                outfile.write("\n")

            # Writes the interpolated data to the same output file
            if interpolate_option is not None and inst_interpolation is not None:
                inst_interpolation.print_interpolated_data(folder=j(output_dir, plot_type, plotfoldername))
            instances.clear()
            resultfiles.clear()
            inputfiles.clear()
