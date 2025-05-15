from model.person import Person
from model.tree import TreeN, NodeN
from typing import List, Optional


class PersonService:
    def __init__(self):
        self.tree = None

    def create_person(self, person: Person, parent_id: Optional[str] = None) -> bool:
        if self.tree is None:
            root_node = NodeN(person=person)
            self.tree = TreeN(root=root_node)
            return True

        return self.tree.create_person(person, parent_id)

    def get_all_persons(self) -> List[Person]:
        if self.tree is None:
            return []
        return self.tree.get_persons()

    def get_person_by_id(self, id: str) -> Optional[Person]:
        persons = self.get_all_persons()
        return next((person for person in persons if person.id == id), None)

    def update_person(self, id: str, person: Person) -> bool:
        if self.tree is None:
            return False
        return self.tree.update_person(id, person)

    def delete_person(self, id: str) -> bool:
        if self.tree is None:
            return False
        return self.tree.delete_person(id)

    def get_persons_with_adult_child(self) -> List[Person]:
        if self.tree is None:
            return []
        return self.tree.get_persons_with_adult_child()

    def filter_persons(self,
                      location_code: Optional[str] = None,
                      typedoc_code: Optional[str] = None,
                      gender: Optional[str] = None) -> List[Person]:
        if self.tree is None:
            return []
        return self.tree.filter_persons(location_code, typedoc_code, gender)

    def get_persons_by_location(self, location_code: str) -> List[Person]:
        if self.tree is None:
            return []
        return self.tree.get_persons_by_location(location_code)