from datetime import datetime, date, timedelta
import database

if __name__ == "__main__":
    userInput = ''
    duration = {}

    # database.dropTable()
    # database.dropDuration()
    # database.createDuration()
    # database.dropDuration()
    # database.createDuration()

    # # mock data
    # database.addActivity('12:00','13:30',"food","this is a note")
    # database.addActivity('13:31','14:00',"study","this is another note")
    # database.addActivity('14:00','15:00',"workout","this is another random note")
    # database.addActivity('15:00','17:00',"food","this is another random note")
    # database.addActivity('17:00','19:00',"study","this is another random note")
    # database.addActivity('19:00','21:00',"game","this is another random note")
    # database.addActivity('21:00','23:00',"study","this is another random note")
    # database.addActivity('23:00','23:59',"prep","this is another random note")

    try:
        while userInput != 'q':
            userInput = input("\nHi, this is a timelog journal program\
            \nPlease enter the character that corresponds to the action you want to perform:\
            \n(1) Add a log entry\n(2) Edit an existing entry\n(3) Delete a log entry\n(4) Print all log entry\
            \n(5) Print time usage summary\n(q) Quit the program\n")

            if userInput == '1': # Add a log entry
                startTime = input("Please enter the start time of this activity ")
                endTime = input("Please enter the end time of this activity ")
                category = input("Please enter the category for this activity ")
                note = input("Please wrtie down a note for this activity ")
                database.addActivity(startTime, endTime, category, note)
                
            elif userInput == '2': # Edit existing log entry
                database.fetchActivity()
                edit_idx = int(input("Please enter the activity id # you wish to edit: "))
                while not 0 < edit_idx <= database.getCount():
                    edit_idx = int(input("Invalid range: Please enter the activity id # you wish to delete: "))
                items = list(database.fetchOne(edit_idx))
                print(f"Start: {items[0]}\nEnd: {items[1]}\nCategory: {items[2]}\nNote: {items[3]}\n")
                user_input = input(("Please select the item you would like to edit\n Start: 0\tEnd: 1\tCategory: 2\t Note: 3\nEnter 'q' to cancel "))
                while user_input != 'q':
                    if 0 <= int(user_input) <= 3:
                        change = input("Please enter the change: ")
                        items[int(user_input)] = change
                    print("Please select the item you would like to edit\n Start: 0\tEnd: 1\tCategory: 2\t Note: 3 ")
                    user_input = input("Enter q to save and exit ")
                database.editActivity(edit_idx, items[0], items[1], items[2], items[3])

            elif userInput == '3': # Delete log entry
                database.fetchActivity()
                del_item = int(input("Please enter the activity id # you wish to delete: "))
                while not 0 < del_item <= database.getCount():
                    del_item = int(input("Invalid range: Please enter the activity id # you wish to delete: "))
                database.deleteActivity(del_item)
            elif userInput == '4': # Print all log entry 
                database.fetchActivity()
            elif userInput == '5': # Print time usage summary
                pass

    except ValueError as err:
        print("Invalid input. Please try again\n", err)

    except TypeError as err:
        print("Invalid input. Please try again\n", err)
        
    database.closeConn()
