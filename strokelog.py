from datetime import datetime
import time
import csv

from pyrow import pyrow

PREFIX = 'workout'


def get_erg(index=0):
    ergs = list(pyrow.find())

    if len(ergs):
        return pyrow.pyrow(ergs[index])


class WorkoutWriter: 

    field_names = ['time', 'distance', 'spm', 'pace']
    force_names = ['Force Plot']

    def __init__(self, file, erg):
        self.erg = erg
        self.file = file
        self.writer = csv.writer(file, delimeter=',')
        self.writer.writerow(field_names + force_names)

    def _update_workout(self):
        self.workout = self.erg.get_workout()

    def _wait_workout(self):
        workout = self.erg.get_workout()

        while workout['state'] == 0:
            time.sleep(1)
            workout = erg.get_workout()
        self.workout = workout

    def _wait_forceplot(self):
        forceplot = erg.get_force_plot()
        workout = self.workout

        #Loop while waiting for drive
        while forceplot['strokestate'] != 2 and workout['state'] == 1:
            time.sleep(0.1)
            forceplot = erg.get_force_plot()
            workout = erg.get_workout()

        self.workout = workout
        self.forceplot = forceplot

    def _loop_drive(force):
        forceplot = self.forceplot
        while forceplot['strokestate'] == 2:
            time.sleep(0.01)
            forceplot = erg.get_force_plot()
            force.extend(forceplot['forceplot'])
        self.forceplot = forceplot

    def run():
        print("Waiting for workout to start ...")

        self._wait_workout()
        print("Workout has begun")

        while self.workout['state'] == 1:
            self._wait_forceplot()

            # Record force data during the drive
            # start of pull (when strokestate first changed to 2)
            force = self.forceplot['forceplot']

            # get monitor data for start of stroke
            monitor = self.erg.get_monitor()

            self._loop_drive(force)

            self.forceplot = self.erg.get_force_plot()
            force.extend(self.forceplot['forceplot'])

            #Write data to write_file
            workoutdata = [monitor[field] for field in self.field_names]
            forcedata = [str(f) for f in force]

            write_file.write(workoutdata + forcedata)

            self._update_workout()


def main():
    erg = get_erg()

    if not erg:
        exit("No ergs found.")

    print("Connected to erg.")

    timestamp = datetime.now()
    filename = f'{PREFIX}_{timestamp}.csv'

    with open(filename, 'w') as write_file:
        workout_writer = WorkoutWriter(write_file, erg)
        workout_writer.run()

    print("Workout has ended")


if __name__ == '__main__':
    main()
