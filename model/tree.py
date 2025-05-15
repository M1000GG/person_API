from typing import List, Optional
from pydantic import BaseModel
from model.person import Person


class NodeN(BaseModel):
    person: Person
    children: List["NodeN"] = []

    def add_child(self, child: "NodeN") -> None:
        self.children.append(child)

    def remove_child_by_id(self, id: str) -> bool:
        for i, child in enumerate(self.children):
            if child.person.id == id:
                self.children.pop(i)
                return True

        for child in self.children:
            if child.remove_child_by_id(id):
                return True

        return False


class TreeN(BaseModel):
    root: NodeN

    def create_person(self, person: Person, parent_id: Optional[str] = None) -> bool:
        new_node = NodeN(person=person)

        if parent_id is None:
            self.root.add_child(new_node)
            return True

        return self._find_and_add_child(self.root, parent_id, new_node)

    def _find_and_add_child(self, node: NodeN, parent_id: str, new_node: NodeN) -> bool:
        if node.person.id == parent_id:
            node.add_child(new_node)
            return True

        for child in node.children:
            if self._find_and_add_child(child, parent_id, new_node):
                return True

        return False

    def get_persons(self) -> List[Person]:
        result = []
        self._traverse_tree(self.root, result)
        return result

    def _traverse_tree(self, node: NodeN, result: List[Person]) -> None:
        result.append(node.person)
        for child in node.children:
            self._traverse_tree(child, result)

    def update_person(self, id: str, person: Person) -> bool:
        return self._update_person_recursively(self.root, id, person)

    def _update_person_recursively(self, node: NodeN, id: str, person: Person) -> bool:
        if node.person.id == id:
            node.person = person
            return True

        for child in node.children:
            if self._update_person_recursively(child, id, person):
                return True

        return False

    def delete_person(self, id: str) -> bool:
        if self.root.person.id == id:
            if not self.root.children:
                return False
            return False

        return self.root.remove_child_by_id(id)

    def get_persons_with_adult_child(self) -> List[Person]:
        result = []
        self._find_persons_with_adult_child(self.root, result)
        return result

    def _find_persons_with_adult_child(self, node: NodeN, result: List[Person]) -> None:
        has_adult_child = any(child.person.age >= 18 for child in node.children)

        for child in node.children:
            self._find_persons_with_adult_child(child, result)

        if has_adult_child:
            result.append(node.person)

    def filter_persons(self, location_code: Optional[str] = None,
                       typedoc_code: Optional[str] = None,
                       gender: Optional[str] = None) -> List[Person]:
        result = []
        self._filter_recursive(self.root, location_code, typedoc_code, gender, result)
        return result

    def _filter_recursive(self, node: NodeN,
                          location_code: Optional[str],
                          typedoc_code: Optional[str],
                          gender: Optional[str],
                          result: List[Person]) -> None:
        matches = True

        if location_code is not None and str(node.person.location.code) != location_code:
            matches = False
        if typedoc_code is not None and str(node.person.typedoc.code) != typedoc_code:
            matches = False
        if gender is not None and node.person.gender != gender:
            matches = False

        if matches:
            result.append(node.person)

        for child in node.children:
            self._filter_recursive(child, location_code, typedoc_code, gender, result)

    def get_persons_by_location(self, location_code: str) -> List[Person]:
        result = []
        self._get_by_location_recursively(self.root, location_code, result)
        return result

    def _get_by_location_recursively(self, node: NodeN, location_code: str, result: List[Person]) -> None:
        if str(node.person.location.code) == location_code:
            result.append(node.person)

        for child in node.children:
            self._get_by_location_recursively(child, location_code, result)