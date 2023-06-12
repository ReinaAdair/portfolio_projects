# Attentance Point Tracker
#       Version 0.2
# Written by Thomas Gordon

# Loads and saves from .json file, allows updating of file through commands, and automatically
# removes any points that have expired in compliance with DS Smith policy

from datetime import date, datetime, timedelta
import json

class PointTracker:
        # Adds and employee to the database
    def addEmployee(database, name):
        empDictItem = {"name" : name, "infractions" : {}, "controlDate" : None, "totalPoints" : 0, "isFlagged" : False}
        database["employees"].append(empDictItem)
        print(f'Added: {name} to current database.')



        # Removes an employee from the database
    def removeEmployee(database, name):
        counter = 0
        for emp in database['employees']:
            if emp['name'].lower() == name.lower():
                confirmation = input(f'Are you sure you want to remove {name} from the current database? y/n ')
                if confirmation.lower() == "yes" or confirmation.lower() == "y":
                    print(emp)
                    database['employees'].pop(counter)
                else:
                    continue
            counter += 1
        print(f'Removed: {name} from current database.')



        # Adds an infraction to a specific employee
    def addInfraction(database, name):
        for emp in database['employees']:
            if emp['name'].lower() == name.lower():
                print(f'Adding infraction to {name}.')
                givenDate = input("What is the date of the infraction? yyyy-mm-dd \nIf infraction was today, type \"today\"\n")

                if givenDate == "today":
                    gDate = date.today()
                else:
                    gDate = datetime.strptime(givenDate, "%Y-%m-%d").date()
                pointvalue = float(input(f'What is the value of the infraction? \n'))
                emp['infractions'][str(gDate)] = pointvalue



        # Removes a specific infraction from an employee
    def removeInfraction(database, name):
        counter = 0
        for emp in database['employees']:
            if emp['name'].lower() == name.lower():
                eminfr = emp['infractions']
                print(f'These are the infractions for {name}\n{eminfr}')
                userChoice = input("Which would date you like to remove? ")

                for infr in emp['infractions']:
                    if infr == userChoice:
                        confirmation = input(f'Are you sure you want to remove {infr} from the current database? y/n ')
                        if confirmation.lower() == "yes" or confirmation.lower() == "y":
                            database['employees'][counter]['infractions'].pop(userChoice)
                            break
            counter += 1



        # Returns list of infractions for a specific employee
    def viewEmployee(database, name):
        for emp in database['employees']:
            if emp['name'].lower() == name.lower():
                emname = emp['name']
                eminfr = emp['infractions']
                emcd = emp['controlDate']
                empts = emp['totalPoints']
                emflag = emp['isFlagged']
                print(f'\nName: {emname} \nInfractions: {eminfr}\nControl Date: {emcd} \nPoints: {empts} \nFlagged: {emflag}')



        # Loops through the JSON variable and checks to see which infractions should be deleted
    def prunePoints(database):
        # Loops through every "employee" in the JSON file
        for i in range(len(database["employees"])):
            empName = database["employees"][i]["name"]
            empInfr = database["employees"][i]["infractions"]
            controlDate = database["employees"][i]["controlDate"]

            today = date.today() # Generates todays date for reference
            infrDates = [] # Keeps track of the Dates tied to Infractions
            oldInfr = [] # Stores infractions that are over 365 days old
            removableInfr = [] # Stores infractions if the 90 day rule is met

            print(f'Processing [{i + 1}/{len(database["employees"])}]')
            #print(empName)

            if empInfr == {}: # If the infractions dictionary is empty it skips that employee
                #print("No infractions \n")
                continue

            for c in empInfr:
                day = datetime.strptime(c, "%Y-%m-%d").date()
                infrDates.append(day)
            infrDates.sort()
                # Newest date is infrDates[-1]
                # Oldest date is infrDates[0]

                # Assigns new control date if employee does not have one assigned
                    # Control date should change to current date if it is used to remove an infracation, or if a new infraction is added
                    # Control date is set to most recent infraction if the employee has no control date
            if controlDate == None:
                    #print("assigning control date...")
                    database["employees"][i].update({"controlDate" : str(infrDates[-1])})
                    controlDate = database["employees"][i]["controlDate"]
                    #print("New Control Date: ", controlDate)
            #print("Employee infractions: ",empInfr)

                # Iterates through the infractions dict for each employee in the JSON variable
            for c in empInfr:
                day = datetime.strptime(c, "%Y-%m-%d").date()
                #print("Todays Date: ", today, " ", type(today))
                #print("Infraction Date: ", day, " ", type(day))
                if (today - day).days >= 365:
                    oldInfr.append(str(day))
                
            for c in oldInfr:
                empInfr.pop(c)

                # Need to reset the dates list to update the already removed ones
            newDates = []
            for c in empInfr:
                day = datetime.strptime(c, "%Y-%m-%d").date()
                newDates.append(day)
            newDates.sort()

                # Set controlDate variable to cdate and current date to day
            cdate = datetime.strptime(controlDate, "%Y-%m-%d").date()
            day = datetime.strptime(c, "%Y-%m-%d").date()

                # If the control date was more than 90 work days ago (estimated 126 total days) remove the oldest infraction
            if (today - cdate).days >= 126: #126
                #print(f"Today: {today} Control Date: {cdate} Diff: {(today - cdate).days}")

                removableInfr.append(str(newDates[0]))

                #print("Old Control Date: ", database["employees"][i]["controlDate"])
                newcdate = (newDates[-1] + timedelta(days=126))
                    
                database["employees"][i].update({"controlDate" : str(newcdate)})
                controlDate = database["employees"][i]["controlDate"]
                    
                #print("New Control Date: ", database["employees"][i]["controlDate"])

            #print("Case 1: ", oldInfr)
            #print("Case 2: ", removableInfr)

            for c in removableInfr:
                empInfr.pop(c)

            database["employees"]



        # Loops through the JSON variable and updates total point count and flagged status for each employee
    def updateTotalPoints(database):
        flaggedEmployees = []
        for i in range(len(database["employees"])):
            totalPoints = 0
            empName = database["employees"][i]["name"] # Pre-defining the path to employee name
            empInfr = database["employees"][i]["infractions"] # Pre-defining the path to employee infractions dict

            if empInfr == {}: # If the infractions dictionary is empty it skips that employee
                continue

            for c in empInfr: # Iterates through the Infractions dictionary for each employee and adds up the total points
                totalPoints += empInfr[c]

            database["employees"][i].update({"totalPoints" : totalPoints}) # Writes the total points value into the JSON variable
            empPoints = database["employees"][i]["totalPoints"] # Pre-defining the path to employee points

                # Flags employee if they have 5 or more points, and unflags them if they have less than 5
            if empPoints >= 5:
                database["employees"][i].update({"isFlagged" : True})
                flaggedEmployees.append(database["employees"][i]["name"])
            elif empPoints < 5:
                database["employees"][i].update({"isFlagged" : False})
            else:
                print("error with checking flag state of employee, ", empName)

        return(flaggedEmployees) # Returns list of employee names for each employee whose isFlagged = True



        # First function that runs, returns JSON file to a variable
    def loadJSON():
        f = open("Employees.json")
        data = json.load(f)
        f.close()
        return(data)



    def saveJSON(database):
        with open("Employees.json", 'w') as out:
            json.dump(database, out)



def main():
    PT = PointTracker
    db = PT.loadJSON() # Set to load the "proto.json" file
    PT.prunePoints(db)
    flaggedEmployees = PT.updateTotalPoints(db)
    print("Currently Flagged Employees: ", flaggedEmployees, '\n')

    commandList = """Commands:
        0 - exit    
        1 - add employee    2 - remove employee
        3 - add infraction  4 - remove infraction
        5 - view employee   6 - view flagged
        9 - help            10 - force exit
    """
    helpList = """0: exit - saves changes and exits the program
    1: add employee - adds an employee to the database
    2: remove employee - removes an employee from the database
    3: add infraction - adds an infraction to a specified employee
    4: remove infraction - removes an infraction from a specified employee
    5: view employee - returns employee information
    6: view flagged - returns the list of flagged employees
    9: help - you are here
    10: force exit - exits the program without saving changes"""

    print(commandList)

    def inputHandler(userInput):
        if userInput == "exit" or userInput == "0": # SAVE AND EXIT
            print("Saving changes...")
            PT.saveJSON(db)

        elif userInput == "add employee" or userInput == "1": # ADD EMPLOYEE
            database = db
            empName = input("Name of new employee? ")
            PT.addEmployee(database, empName)

        elif userInput == "remove employee" or userInput == "2": # REMOVE EMPLOYEE
            database = db
            empName = input("Which employee would you like to remove? ")
            PT.removeEmployee(database, empName)

        elif userInput == "add infraction" or userInput == "3": # ADD INFRACTION
            database = db
            empName = input("Which employee would you like to add an infraction to? ")
            PT.addInfraction(database, empName)
            flaggedEmployees = PT.updateTotalPoints(db)

        elif userInput == "remove infraction" or userInput == "4": # REMOVE INFRACTION
            database = db
            empName = input("Which employee would you like to remove an infraction from? ")
            PT.removeInfraction(database, empName)
            flaggedEmployees = PT.updateTotalPoints(db)

        elif userInput == "view employee" or userInput == "5": # VIEW EMPLOYEE
            database = db
            empName = input("Which employee would you like to view? ")
            PT.viewEmployee(database, empName)

        elif userInput == "view flagged" or userInput == "6": # VIEW FLAGGED LIST
            flaggedEmployees = PT.updateTotalPoints(db)
            print("Currently Flagged Employees: ", flaggedEmployees)

        elif userInput == "help" or userInput == "9": # HELP
            print(helpList)

        elif userInput == "force exit" or userInput == "10": # FORCE EXIT
            print("Automatic and manual alterations to records will not be saved.")
            print("If you wish to continue without saving please enter \"no save\"...")

        else:
            print("Command not recognized")

    userInput = ""
    while userInput != "exit" and userInput != "no save" and userInput != "0":
        print(commandList)
        userInput = input("\nPlease select a command... ").lower()
        inputHandler(userInput)

main()