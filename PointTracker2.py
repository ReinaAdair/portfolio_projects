from datetime import date, datetime, timedelta
import json

class PointTracker:
        # Adds and employee to the database
    def addEmployee(database, name):
        pass



        # Removes an employee from the database
    def removeEmployee(database, name):
        pass



        # Adds an infraction to a specific employee
    def addInfraction(database, name, dateof, points):
        pass



        # Removes a specific infraction from an employee
    def removeInfraction(database, name):
        pass



        # Returns list of infractions for a specific employee
    def viewInfractions(database, name):
        pass



        # Loops through the JSON variable and checks to see which infractions should be deleted
    def prunePoints(database):
        for i in database["employees"]:
            empName = database["employees"][i]["name"]
            empInfr = database["employees"][i]["infractions"]
            controlDate = database["employees"][i]["controlDate"]

            today = date.today()
            infrDates = []
            oldInfr = []
            removableInfr = []

            print(empName)

            if empInfr == {}: # If the infractions dictionary is empty it skips that employee
                print('\n')
                continue

            for c in empInfr:
                day = datetime.strptime(c, "%Y-%m-%d").date()
                infrDates.append(day)
            infrDates.sort()
            #print("Dates list: ", infrDates)
                # Newest date is infrDates[-1]
                # Oldest date is infrDates[0]

                # Assigns new control date if employee does not have one assigned
                    # Control date should change to current date if it is used to remove an infracation, or if a new infraction is added
            if controlDate == None:
                    print("assigning control date...")
                    database["employees"][i].update({"controlDate" : str(infrDates[-1])})
                    controlDate = database["employees"][i]["controlDate"]
                    print("New Control Date: ", controlDate)

            print("Employee infractions: ",empInfr)

                # Iterates through the infractions dict for each employee in the JSON variable
            for c in empInfr:
                day = datetime.strptime(c, "%Y-%m-%d").date()
                #print("Todays Date: ", today, " ", type(today))
                #print("Infraction Date: ", day, " ", type(day))
                if (today - day).days >= 365:
                    #print("Delete ", day)
                    oldInfr.append(str(day))
                
            for c in oldInfr:
                empInfr.pop(c)

                # Need to reset the dates list to update the already removed ones
            newDates = []
            for c in empInfr:
                day = datetime.strptime(c, "%Y-%m-%d").date()
                newDates.append(day)
            newDates.sort()

            for c in empInfr:
                cdate = datetime.strptime(controlDate, "%Y-%m-%d").date()
                day = datetime.strptime(c, "%Y-%m-%d").date()

                if (today - cdate).days >= 90:
                    #print("Delete 2 ", day)
                    #print(f"Today: {today} Control Date: {cdate} Diff: {(today - cdate).days}")
                    
                    removableInfr.append(str(newDates[0]))

                    #print("Control Date: ", database["employees"][i]["controlDate"])
                    newcdate = (newDates[-1] + timedelta(days=90))
                    
                    database["employees"][i].update({"controlDate" : str(newcdate)})
                    controlDate = database["employees"][i]["controlDate"]
                    
                    print("Control Date: ", database["employees"][i]["controlDate"])


            #print("Case 1: ", oldInfr)
            #print("Case 2: ", removableInfr)

            for c in removableInfr:
                empInfr.pop(c)

            database["employees"]

            print("Infractions after prune: ", empInfr)
            print('\n')



        # Loops through the JSON variable and updates total point count and flagged status for each employee
    def updateTotalPoints(database):
        flaggedEmployees = []
        for i in database["employees"]:
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



    def checkDates(dateOne, dateTwo):
        print(dateOne)
        pass



        # First function that runs, returns JSON file to a variable
    def loadJSON():
        f = open("Point Tracker\proto.json")
        data = json.load(f)
        f.close()
        return(data)



    def saveJSON(database):
        with open("Point Tracker/protosave.json", 'w') as out:
            json.dump(database, out)



def main():
    PT = PointTracker
    db = PT.loadJSON()
    PT.prunePoints(db)
    flaggedEmployees = PT.updateTotalPoints(db)
    print(flaggedEmployees)
    PT.saveJSON(db)

main()