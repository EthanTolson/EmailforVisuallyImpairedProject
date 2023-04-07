import pymongo

class DB_query():
    def __init__(self, username):
        self.client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@{cluster}.mongodb.net/?retryWrites=true&w=majority")
        self.username = username

    def get_addresses(self):
        """
        returns a list of email addresses in the users address book
        """
        addresses = [""]
        query = {"username": self.username}
        result = self.client["seniorproject"]['addressbook'].find(query)

        for record in result:
            addresses.append(record['contact'])

        return addresses

    def add_to_address_book(self, address):
        """
        adds address to database returns true if document was successfully inserted
        """
        # Define the document to be inserted
        document = {"username": self.username, "contact": address}

        # Insert the document into the collection
        
        result = self.client["seniorproject"]['addressbook'].insert_one(document)

        if result.inserted_id:
            return True
        else:
            return False

    def save_draft(self, to, subj, body):
        """
        adds draft to database returns true if document was successfully inserted
        """
        # Define the document to be inserted
        document = {"user": self.username, "to": to, "subj": subj, "body": body}

        # Insert the document into the collection
        
        result = self.client["seniorproject"]['drafts'].insert_one(document)

        if result.inserted_id:
            return True
        else:
            return False

    def get_drafts(self):
        drafts = [["", "", ""]]

        query = {"user": self.username}
        result = self.client["seniorproject"]['drafts'].find(query)

        for record in result:
            drafts.append([record['to'], record["subj"], record["body"]])

        return drafts
