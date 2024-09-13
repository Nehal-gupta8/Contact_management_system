import csv

class Contact:
    def __init__(self, name, phone_number, email, group="General", favorite=False):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.group = group
        self.favorite = favorite

    def __str__(self):
        return f"{self.name},{self.phone_number},{self.email},{self.group},{self.favorite}"

class ContactBook:
    def __init__(self, filename="contacts.csv"):
        self.filename = filename
        self.contacts = {}
        self.unsaved_changes = False
        self.load_contacts()

    def load_contacts(self):
        try:
            with open(self.filename, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        name, phone_number, email, group, favorite = row
                        self.contacts[name] = Contact(name, phone_number, email, group, favorite == "True")
        except FileNotFoundError:
            print(f"{self.filename} does not exist. Starting with an empty contact book.")

    def save_contacts(self):
        """Batch save all contacts to the file."""
        with open(self.filename, "w", newline='') as file:
            writer = csv.writer(file)
            for contact in sorted(self.contacts.values(), key=lambda x: (not x.favorite, x.name)):
                writer.writerow([contact.name, contact.phone_number, contact.email, contact.group, contact.favorite])
        self.unsaved_changes = False

    def add_contact(self, name, phone_number, email, group="General", favorite=False):
        """Add a new contact to the contact book."""
        self.contacts[name] = Contact(name, phone_number, email, group, favorite)
        self.unsaved_changes = True

    def search_contact(self, query):
        """Search by name, phone number, or email. Partial matches are also allowed."""
        results = []
        query = query.lower()
        for contact in self.contacts.values():
            if (query in contact.name.lower() or query in contact.phone_number or query in contact.email.lower()):
                results.append(contact)
        return results

    def update_contact(self, name, new_phone_number=None, new_email=None, new_group=None, favorite=None):
        """Update an existing contact's details."""
        if name in self.contacts:
            contact = self.contacts[name]
            if new_phone_number:
                contact.phone_number = new_phone_number
            if new_email:
                contact.email = new_email
            if new_group:
                contact.group = new_group
            if favorite is not None:
                contact.favorite = favorite
            self.unsaved_changes = True
            return True
        return False

    def delete_contact(self, name):
        """Delete a contact by name."""
        if name in self.contacts:
            del self.contacts[name]
            self.unsaved_changes = True
            return True
        return False

    def list_contacts(self):
        """Return all contacts, with favorites at the top."""
        return sorted(self.contacts.values(), key=lambda x: (not x.favorite, x.name))

    def exit_program(self):
        """Exit the program and prompt to save unsaved changes."""
        if self.unsaved_changes:
            save_now = input("You have unsaved changes. Do you want to save before exiting? (y/n): ").lower()
            if save_now == 'y':
                self.save_contacts()

    def display_contacts(self, contacts):
        """Display contacts in a tabular format."""
        if contacts:
            print(f"{'Name':<15}{'Phone':<15}{'Email':<25}{'Group':<10}{'Favorite'}")
            print("=" * 65)
            for contact in contacts:
                favorite = "Yes" if contact.favorite else "No"
                print(f"{contact.name:<15}{contact.phone_number:<15}{contact.email:<25}{contact.group:<10}{favorite}")
        else:
            print("No contacts found.")

def main():
    contact_book = ContactBook()

    while True:
        print("\n1. Add Contact")
        print("2. Update Contact")
        print("3. Delete Contact")
        print("4. List Contacts")
        print("5. Search Contact")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter name: ")
            phone_number = input("Enter phone number: ")
            email = input("Enter email: ")
            group = input("Enter group (Family/Friends/Work or leave blank for 'General'): ") or "General"
            favorite = input("Mark as favorite? (y/n): ").lower() == 'y'
            contact_book.add_contact(name, phone_number, email, group, favorite)
            print(f"Contact '{name}' added successfully.")
        
        elif choice == '2':
            name = input("Enter name to update: ")
            new_phone_number = input("Enter new phone number (or press enter to skip): ")
            new_email = input("Enter new email (or press enter to skip): ")
            new_group = input("Enter new group (or press enter to skip): ")
            favorite = input("Mark as favorite? (y/n or press enter to skip): ")
            favorite = favorite.lower() == 'y' if favorite else None
            if contact_book.update_contact(name, new_phone_number, new_email, new_group, favorite):
                print("Contact updated successfully.")
            else:
                print("Contact not found.")
        
        elif choice == '3':
            name = input("Enter name to delete: ")
            if contact_book.delete_contact(name):
                print("Contact deleted successfully.")
            else:
                print("Contact not found.")
        
        elif choice == '4':
            contacts = contact_book.list_contacts()
            contact_book.display_contacts(contacts)
        
        elif choice == '5':
            query = input("Enter name, phone number, or email to search: ")
            results = contact_book.search_contact(query)
            if results:
                contact_book.display_contacts(results)
            else:
                print("No matching contacts found.")
        
        elif choice == '6':
            contact_book.exit_program()
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
