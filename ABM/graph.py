# !/usr/bin/python
# 1/7/2019

"""
This document runs the server and helps visualize the agents.
"""

from excel_export_summary import *
from excel_export_summary_humans import *
from excel_export_density_plot import *
import matplotlib.pyplot as plt
import numpy as np
from model import *
from families import demographic_structure_list, female_list, male_maingroup_list, reproductive_female_list, moved_list
from humans import hh_size_list, human_birth_list, human_death_list, human_marriage_list,\
    single_male_list, married_male_list, \
    labor_list, total_migration_list, total_re_migration_list
from fnnr_config_file import human_setting, year_setting, random_walk_graph_setting, plot_setting
import os

monkey_population_list = []
monkey_birth_count = []
monkey_death_count = []

model = Movement()  # run the model
time = 73 * year_setting # 73 time-steps of 5 days each for 10 years, 730 steps total
erase_summary()  # clears the Excel file to overwrite
erase_human_summary()
# erase_density_plot()  # delete files manually since they iterate when multiple are created
for t in range(time):  # for each time-step in the time we just defined,
    monkey_population_list.append(model.number_of_monkeys)
    monkey_birth_count.append(model.monkey_birth_count)
    monkey_death_count.append(model.monkey_death_count)
    model.step()  # see model.step() in model.py; monkey agents age, family-pixel agents move
    print('Loading, Progress', t, '/', time)
    if t == 1 or t % 20 == 0:  # save beginning structure, then every 100 days thereafter
        save_summary(t, model.number_of_monkeys, model.monkey_birth_count, model.monkey_death_count,
                 demographic_structure_list, female_list, male_maingroup_list, reproductive_female_list)
        save_summary_humans(t, model.number_of_humans, len(human_birth_list), len(human_death_list), len(human_marriage_list),
                            len(labor_list),
                            len(single_male_list), len(married_male_list), sum(total_migration_list))  # 94 households


if random_walk_graph_setting == True:  # disabled or enabled according to fnnr_config_file.py
    # this should only be run with 1 family at a time or else the graphs will be messed up
    if t == 73 * 1:
        save_density_plot(moved_list, 1)
    if t == 73 * 3:
        save_density_plot(moved_list, 3)
    if t == 73 * 5:
        save_density_plot(moved_list, 5)

movement_session_id = 0
currentpath = str(inspect.getfile(inspect.currentframe()))[:-8]  # 'removes graph.py' at end
os.chdir(currentpath)
while os.path.exists(str(os.getcwd()) + "export_density_plot_" + human_setting + str(movement_session_id) + ".csv"):
    movement_session_id += 1
save_density_plot(moved_list, movement_session_id)

save_summary(t, model.number_of_monkeys, model.monkey_birth_count, model.monkey_death_count,
             demographic_structure_list, female_list, male_maingroup_list, reproductive_female_list)
save_summary_humans(t, model.number_of_humans, len(human_birth_list), len(human_death_list),
                    len(human_marriage_list), len(labor_list),
                    len(single_male_list), len(married_male_list), sum(total_migration_list))  # 94 households total
# functions above are called again after the last step

plt.subplot(211)
age_category_list = ('0-1', '1-3', '3-7', '7-10', '10-25', '25+')
index = np.arange(len(age_category_list))
width = 0.5  # width of each bar
plt.bar(index, demographic_structure_list, width, align = 'center')
plt.xticks(index, age_category_list)
plt.title('Age Structure in the FNNR After ' + str(time) + ' Steps')
plt.xlabel('Age')
plt.ylabel('# of Monkeys')
print('Age Structure Count || 0-1: %i | 1-3: %i | 3-7: %i | 7-10: %i | 10-25: %i | 25+: %i' %
      (demographic_structure_list[0], demographic_structure_list[1],
       demographic_structure_list[2], demographic_structure_list[3],
       demographic_structure_list[4], demographic_structure_list[5]))

# Percentages of each age category
print(
str("Age 0-1: " + str(round(demographic_structure_list[0] / sum(demographic_structure_list) * 100, 2)) + "% | "),
str("Age 1-3: " + str(round(demographic_structure_list[1] / sum(demographic_structure_list) * 100, 2)) + "% | "),
str("Age 3-7: " + str(round(demographic_structure_list[2] / sum(demographic_structure_list) * 100, 2)) + "% | "),
str("Age 7-10: " + str(round(demographic_structure_list[3] / sum(demographic_structure_list) * 100, 2)) + "% | "),
str("Age 10-25: " + str(round(demographic_structure_list[4] / sum(demographic_structure_list) * 100, 2)) + "% | "),
str("Age 25+: " + str(round(demographic_structure_list[5] / sum(demographic_structure_list) * 100, 2)) + "%"))

plt.subplot(212)
gender_category_list = ('Rep. Females', 'Total Females', 'Main Group Males')
index2 = np.arange(len(gender_category_list))
# print(gender_category_list)
width = 0.5
plt.bar(index2, [len(reproductive_female_list), len(female_list), len(male_maingroup_list)], width, align = 'center')
plt.xticks(index2, gender_category_list)
plt.title('Gender Structure in the FNNR After ' + str(time) + ' Steps')
plt.ylabel('# of Monkeys')
print('Gender Structure Count || Reproductive Females: %i | Total Females: %i | Main-group Males: %i' %
      (len(reproductive_female_list), len(female_list), len(male_maingroup_list)))
plt.tight_layout()  # needed to make the graph look neat
plt.figure()  # each instance of plt.figure() sets a graph in a new window

plt.subplot(2, 2, 1)
plt.plot(np.array(range(time)), np.array(monkey_population_list))
plt.title('GGM Population in the FNNR')
plt.xlabel('5-Day Intervals (Steps)')
plt.ylabel('Number of Monkeys')

plt.subplot(2, 2, 2)
plt.plot(np.array(range(time)), np.array(monkey_birth_count))
plt.title('GGM Births in the FNNR')
plt.xlabel('5-Day Intervals (Steps)')
plt.ylabel('Number of Births')

plt.subplot(2, 2, 3)
plt.plot(np.array(range(time)), np.array(monkey_death_count))
plt.title('GGM Deaths in the FNNR')
plt.xlabel('5-Day Intervals (Steps)')
plt.ylabel('Number of Deaths')
plt.tight_layout()

if plot_setting == True:
    plt.show()  # shows all plots at once