from xmlrpc.client import ServerProxy

SERVER = "http://localhost:8000"

def main():
    server = ServerProxy(SERVER)

    while True:
        print("1. Get note")
        print("2. Add note")
        print("3. Fetch wikipedia summary")
        print("4. Fetch wikipedia page")
        print("5. Add note with wikipedia summary")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            topic = input("Enter topic: ")
            notes = server.get_note(topic)
            if notes:
                    print("Name: ", notes[0])
                    print("Text: ", notes[1])
                    print("Date: ", notes[2])
                    print()
            else:
                print("No notes found")
        elif choice == "2":
            topic = input("Enter topic: ")
            name = input("Enter name: ")
            text = input("Enter text: ")
            if server.add_note(topic, name, text):
                print("Note added")
            else:
                print("Error adding note")
        elif choice == "3":
            topic = input("Enter topic: ")
            print(server.fetch_wikipedia_summary(topic))
        elif choice == "4":
            topic = input("Enter topic: ")
            print(server.fetch_wikipedia_page(topic))
        elif choice == "5":
            topic = input("Enter topic: ")
            if server.add_wikipedia_summary(topic):
                print("Note added")
            else:
                print("Error adding note")
        elif choice == "0":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()