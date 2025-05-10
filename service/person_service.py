from model.person import Person
from model.tree import TreeN, NodeN
from typing import List, Optional


class PersonService:
    def __init__(self):
        # Initialize an empty tree to store persons
        # We need to create a dummy root to initialize the tree
        self.tree = None

    def create_person(self, person: Person, parent_id: Optional[str] = None) -> bool:
        # Create a new person in the tree
        # If parent_id is provided, the person will be a child of that parent
        # If not, will be a child of the root or become the root if tree is empty

        # If tree doesn't exist yet, create it with the first person as root
        if self.tree is None:
            root_node = NodeN(person=person)
            self.tree = TreeN(root=root_node)
            return True

        return self.tree.create_person(person, parent_id)

    def get_all_persons(self) -> List[Person]:
        # Get all persons in the tree
        if self.tree is None:
            return []
        return self.tree.get_persons()

    def get_person_by_id(self, id: str) -> Optional[Person]:
        # Get a specific person by ID
        persons = self.get_all_persons()
        for person in persons:
            if person.id == id:
                return person
        return None

    def update_person(self, id: str, person: Person) -> bool:
        # Update an existing person's information
        if self.tree is None:
            return False
        return self.tree.update_person(id, person)

    def delete_person(self, id: str) -> bool:
        # Delete a person from the tree
        if self.tree is None:
            return False
        return self.tree.delete_person(id)

    def get_adults_with_adult_children(self) -> List[Person]:
        # Get all persons who have at least one adult child (18+ years)
        if self.tree is None:
            return []
        return self.tree.get_persons_with_adult_child()

    def filter_persons(self, location_code: str = None, typedoc_code: str = None, gender: str = None) -> List[Person]:
        # Filter persons by location code, document type code, and/or gender
        all_persons = self.get_all_persons()
        filtered_persons = []

        for person in all_persons:
            matches = True

            if location_code is not None and str(person.location.code) != location_code:
                matches = False
            if typedoc_code is not None and str(person.typedoc.code) != typedoc_code:
                matches = False
            if gender is not None and person.gender != gender:
                matches = False

            if matches:
                filtered_persons.append(person)

        return filtered_persons

    def get_persons_by_location(self, location_code: str) -> List[Person]:
        # Get all persons from a specific location
        if self.tree is None:
            return []
        return self.tree.get_persons_by_location(location_code)