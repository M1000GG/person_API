from typing import List, Optional
from pydantic import BaseModel, Field
from model.person import Person


class NodeN(BaseModel):
    person: Person
    children: List["NodeN"] = []

    def add_child(self, child: "NodeN") -> None:
        # Add a child to the Node
        self.children.append(child)

    def remove_child_by_id(self, id: str) -> bool:
        # Remove a child from the node with person.id
        for i, child in enumerate(self.children):
            if child.person.id == id:
                self.children.pop(i)
                return True

        # If not found at this level on tree, search recursively
        for child in self.children:
            if child.remove_child_by_id(id):
                return True

        # If don't find any child in the tree, returns false
        return False


class TreeN(BaseModel):
    # Create structure of the tree
    root: NodeN

    # Create a new person
    def create_person(self, person: Person, parent_id: Optional[str] = None) -> bool:
        new_node = NodeN(person=person)

        # If parent_id is not provided, add as a root's child
        if parent_id is None:
            self.root.add_child(new_node)
            return True

        # Find the parent node and add the new person as a child
        return self.find_and_add_child(self.root, parent_id, new_node)

    def find_and_add_child(self, node: NodeN, parent_id: str, new_node: NodeN) -> bool:
        #Find a node by id an add a child to it
        if node.person.id == parent_id:
            node.add_child(new_node)
            return True

        # If not found at this level on tree, search recursively
        for child in node.children:
            if self.find_and_add_child(child, parent_id, new_node):
                return True

        # If don't find any parent_id in the tree, returns false
        return False

    def get_persons(self) -> list[Person]:
        #Get all the persons in the tree
        # Call the next function
        result = []
        self.traverse_tree(self.root, result)
        return result

    def traverse_tree(self, node: NodeN, result: list[Person]) -> None:
        # Traverse the tree recursively
        result.append(node.person)
        for child in node.children:
            self.traverse_tree(child, result)

    def update_person(self, id:str, person: Person) -> bool:
        # Update a person in the tree
        return self.update_person_recursively(self.root, id, person)

    def update_person_recursively(self, node: NodeN, id:str, person: Person) -> bool:
        # Update a person in the tree recursively
        if node.person.id == id:
            # Update the person but keep the same children
            node.person = person
            return True

        # If not found at this level on tree, search recursively
        for child in node.children:
            if self.update_person_recursively(child, id, person):
                return True

        # If don't find any node in the tree, returns false
        return False

    def delete_person(self, id:str) -> bool:
        # Delete a person from the tree
        # In case of root is being deleted
        if self.root.person.id == id:
            # If root has no children, clear the tree
            if not self.root.children:
                # No se puede eliminar la raíz directamente, devolver False
                return False

            # Otherwise can't delete root with children
            return False

        # Try to remove from any node in the tree
        return self.root.remove_child_by_id(id)

    def get_persons_with_adult_child(self) -> list[Person]:
        # Get persons who have at least one child that is age > 18
        # Call the recursively function
        result = []
        self.find_persons_with_adult_child(self.root, result)
        return result

    def find_persons_with_adult_child(self, node: NodeN, result: list[Person]) -> None:
        # Find persons with adult child recursively
        has_adult_child = False

        # Calculate adult or not
        for child in node.children:
            if child.person.age >= 18:
                has_adult_child = True
            self.find_persons_with_adult_child(child, result)

        # Append to empty list 'result'
        if has_adult_child:
            result.append(node.person)

    def filter_by_location_typedoc_gender(self, loc:str, td:str, g:str) -> List[Person]:
        # Filter persons by location, typedoc and gender
        # Call the recursively function
        result = []
        self.filter_recursive(self.root, loc, td, g, result)
        return result

    def filter_recursive(self, node: NodeN, loc: str, td:str, g: str, result: List[Person]) -> None:
        # Filter recursively
        if str(node.person.location.code) == loc and str(node.person.typedoc.code) == td and node.person.gender == g:
            result.append(node.person)

        for child in node.children:
            self.filter_recursive(child, loc, td, g, result)

    def get_persons_by_location(self, location:str) -> list[Person]:
        # Get persons by location code
        # Call the recursively function
        result = []
        self.get_by_location_recursively(self.root, location, result)
        return result

    def get_by_location_recursively(self, node: NodeN, location: str, result: list[Person]) -> None:
        # Get by location recursively
        if str(node.person.location.code) == location:
            result.append(node.person)

        for child in node.children:
            self.get_by_location_recursively(child, location, result)