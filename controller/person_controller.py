from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from model.person import Person
from model.typedoc import Typedoc
from model.location import Location
from service.person_service import PersonService
from service.location_service import LocationService
from service.typedoc_service import TypedocService

person_router = APIRouter(prefix="/persons", tags=["persons"])

# Will store the services that help us manage person data
person_service_instance: PersonService = None
location_service_instance: LocationService = None
typedoc_service_instance: TypedocService = None


# Save services to be used later in other parts of the api
def set_person_service(service: PersonService):
    global person_service_instance
    person_service_instance = service


def set_location_typedoc_services(location_service: LocationService, typedoc_service: TypedocService):
    global location_service_instance, typedoc_service_instance
    location_service_instance = location_service
    typedoc_service_instance = typedoc_service


# Provide the saved services when needed
def get_person_service():
    return person_service_instance


def get_location_service_for_persons():
    return location_service_instance


def get_typedoc_service_for_persons():
    return typedoc_service_instance


@person_router.post("/", response_model=bool)
def create_person(
        person: Person,
        parent_id: Optional[str] = None,
        person_service: PersonService = Depends(get_person_service),
        location_service: LocationService = Depends(get_location_service_for_persons),
        typedoc_service: TypedocService = Depends(get_typedoc_service_for_persons)
):
    # Validate location exists
    location = location_service.get_location_by_code(person.location.code)
    if not location:
        raise HTTPException(status_code=404, detail=f"Location with code {person.location.code} not found")

    # Validate typedoc exists
    typedoc = typedoc_service.get_typedoc_by_code(person.typedoc.code)
    if not typedoc:
        raise HTTPException(status_code=404, detail=f"Document type with code {person.typedoc.code} not found")

    # Validate if parent exists when provided
    if parent_id:
        parent = person_service.get_person_by_id(parent_id)
        if not parent:
            raise HTTPException(status_code=404, detail=f"Parent person with ID {parent_id} not found")

    # Validate if person with same ID already exists
    existing_person = person_service.get_person_by_id(person.id)
    if existing_person:
        raise HTTPException(status_code=409, detail=f"Person with ID {person.id} already exists")

    # Create the person
    result = person_service.create_person(person, parent_id)
    return result


@person_router.get("/", response_model=List[Person])
def get_all_persons(
        person_service: PersonService = Depends(get_person_service)
):
    # Get all persons in the system
    return person_service.get_all_persons()


@person_router.get("/{id}", response_model=Person)
def get_person_by_id(
        id: str,
        person_service: PersonService = Depends(get_person_service)
):
    # Get a specific person by ID
    person = person_service.get_person_by_id(id)
    if not person:
        raise HTTPException(status_code=404, detail=f"Person with ID {id} not found")
    return person


@person_router.put("/{id}", response_model=bool)
def update_person(
        id: str,
        person: Person,
        person_service: PersonService = Depends(get_person_service),
        location_service: LocationService = Depends(get_location_service_for_persons),
        typedoc_service: TypedocService = Depends(get_typedoc_service_for_persons)
):
    # Check if person exists
    existing_person = person_service.get_person_by_id(id)
    if not existing_person:
        raise HTTPException(status_code=404, detail=f"Person with ID {id} not found")

    # Validate location exists
    location = location_service.get_location_by_code(person.location.code)
    if not location:
        raise HTTPException(status_code=404, detail=f"Location with code {person.location.code} not found")

    # Validate typedoc exists
    typedoc = typedoc_service.get_typedoc_by_code(person.typedoc.code)
    if not typedoc:
        raise HTTPException(status_code=404, detail=f"Document type with code {person.typedoc.code} not found")

    # Update the person
    result = person_service.update_person(id, person)
    return result


@person_router.delete("/{id}", response_model=bool)
def delete_person(
        id: str,
        person_service: PersonService = Depends(get_person_service)
):
    # Check if person exists
    existing_person = person_service.get_person_by_id(id)
    if not existing_person:
        raise HTTPException(status_code=404, detail=f"Person with ID {id} not found")

    # Delete the person
    result = person_service.delete_person(id)
    if not result:
        raise HTTPException(status_code=400,
                            detail=f"Cannot delete person with ID {id}. The person might be the root with children.")
    return result


@person_router.get("/filter/by-criteria", response_model=List[Person])
def filter_persons(
        location_code: Optional[str] = Query(None, description="Location code to filter by"),
        typedoc_code: Optional[str] = Query(None, description="Document type code to filter by"),
        gender: Optional[str] = Query(None, description="Gender to filter by (M/F)"),
        person_service: PersonService = Depends(get_person_service)
):
    # Filter persons by criteria
    return person_service.filter_persons(location_code, typedoc_code, gender)


@person_router.get("/filter/with-adult-children", response_model=List[Person])
def get_persons_with_adult_children(
        person_service: PersonService = Depends(get_person_service)
):
    # Get persons who have at least one adult child
    return person_service.get_adults_with_adult_children()


@person_router.get("/filter/by-location/{location_code}", response_model=List[Person])
def get_persons_by_location(
        location_code: str,
        person_service: PersonService = Depends(get_person_service),
        location_service: LocationService = Depends(get_location_service_for_persons)
):
    # Validate location exists
    location = location_service.get_location_by_code(int(location_code))
    if not location:
        raise HTTPException(status_code=404, detail=f"Location with code {location_code} not found")

    # Get persons by location
    return person_service.get_persons_by_location(location_code)