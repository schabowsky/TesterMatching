import sys
import csv
import configparser


class TesterMatching:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.TESTERS_FILE = config["DEFAULT"]["TESTERS_FILE"]
        self.DEVICES_FILE = config["DEFAULT"]["DEVICES_FILE"]
        self.BUGS_FILE = config["DEFAULT"]["BUGS_FILE"]
        self.TESTER_DEVICE_FILE = config["DEFAULT"]["TESTER_DEVICE_FILE"]
        self.load_options()

    def load_options(self):
        self.countries = self.get_options(self.TESTERS_FILE, "country")
        self.devices = self.get_options(self.DEVICES_FILE, "description")

    def get_options(self, filename=None, criterion_name=None):
        if not filename or not criterion_name:
            print(e)
            sys.exit("Program was unable to find any data.")

        try:
            with open(filename, "r") as csvfile:
                reader = csv.reader(csvfile)
                criterion_id = next(reader).index(criterion_name)

                options = []
                for row in reader:
                    if row[criterion_id] not in options:
                        options.append(row[criterion_id])
        except Exception as e:
            print(e)
            sys.exit("Program was unable to find any data.")

        return options

    def get_rows_from_csv(self, filename=None, criterion_name=None, criterion=[]):
        if not filename:
            print(e)
            sys.exit("Program was unable to find any data.")

        try:
            with open(filename, "r") as csvfile:
                reader = csv.reader(csvfile)
                if criterion_name is not None:
                    criterion_id = next(reader).index(criterion_name)

                for row in reader:
                    if len(criterion) > 0:
                        if row[criterion_id] in criterion:
                            yield row
                    else:
                        yield row
        except Exception as e:
            print(e)
            sys.exit("Program was unable to find any data.")

    def get_data(self, tester_criteria, device_criteria):
        # Iterate over Testers from specific country
        for tester in self.get_rows_from_csv(self.TESTERS_FILE, "country", tester_criteria):
            counter = 0
            any_test = False
            # Iterate over every tester_device pair
            for row in self.get_rows_from_csv(filename=self.TESTER_DEVICE_FILE):
                if row[0] == tester[0]:
                    # Iterate over specific Devices
                    for device in self.get_rows_from_csv(self.DEVICES_FILE, "description", device_criteria):
                        if row[1] == device[0]:
                            # In case there was a test without any bugs
                            any_test = True
                            for bug in self.get_rows_from_csv(self.BUGS_FILE, "bugId", []):
                                if bug[1] == device[0] and bug[2] == tester[0]:
                                    counter += 1
            if any_test:
                try:
                    yield " ".join(["User:", tester[1], tester[2], "| Experience:", str(counter)])
                except Exception as e:
                    sys.exit("Program was unable to return more results!")


def main():
    tester_matching = TesterMatching()

    print("Find Testers based on your criteria!")

    country_criteria = []
    country_input = ""
    print("Select a country:")
    while country_input != "Y" or len(country_criteria) == 0:
        print("[0] ALL")
        for index, country in enumerate(tester_matching.countries):
            print("[" + str(index + 1) + "]", country)
        country_input = input("Insert index: ")

        if country_input == "0":
            country_criteria = []
            break
        try:
            country_criteria.append(tester_matching.countries[int(country_input) - 1])
            print("Insert 'Y' to select next criteria or choose another country.")
        except Exception as inst:
            if country_input == "Y":
                country_criteria = set(country_criteria)
                break
            print("Insert a number or 'Y'!")
            continue

    device_criteria = []
    device_input = ""
    print("Select a device:")
    while device_input != "Y" or len(device_criteria) == 0:
        print("[0] ALL")
        for index, device in enumerate(tester_matching.devices):
            print("[" + str(index + 1) + "]", device)
        device_input = input("Insert index: ")

        if device_input == "0":
            device_criteria = []
            break
        try:
            device_criteria.append(tester_matching.devices[int(device_input) - 1])
            print("Insert 'Y' to get results or choose another device.")
        except Exception as inst:
            if device_input == "Y":
                device_criteria = set(device_criteria)
                break
            print("Insert a number or 'Y'!")
            continue

    print("\nResults:")
    for match in tester_matching.get_data(country_criteria, device_criteria):
        print(match)


main()
