"""Creational - Builder: HR employee onboarding system.

Statement: https://courses.dallard.tech/sys_design/creational_pattern/
Run: python3 builder_employee.py
"""
from __future__ import annotations

from dataclasses import dataclass


# 1. The product: a plain data container holding the final record
@dataclass
class Employee:
    first_name: str
    last_name: str
    email: str
    department: str
    position: str
    salary: float
    start_date: str
    manager_id: int | None = None
    phone: str | None = None
    address: str | None = None
    emergency_contact: str | None = None
    has_parking: bool = False
    has_laptop: bool = False
    has_vpn_access: bool = False
    has_admin_rights: bool = False
    office_location: str | None = None
    contract_type: str = "permanent"


# 2. The builder: small chainable methods, each returns self
class EmployeeBuilder:
    def __init__(self) -> None:
        self._data: dict = {"start_date": None}

    def with_name(self, first_name: str, last_name: str) -> EmployeeBuilder:
        self._data.update(first_name=first_name, last_name=last_name)
        return self

    def with_email(self, email: str) -> EmployeeBuilder:
        self._data["email"] = email
        return self

    def with_job(self, department: str, position: str, salary: float) -> EmployeeBuilder:
        self._data.update(department=department, position=position, salary=salary)
        return self

    def starting_on(self, start_date: str) -> EmployeeBuilder:
        self._data["start_date"] = start_date
        return self

    def with_manager(self, manager_id: int) -> EmployeeBuilder:
        self._data["manager_id"] = manager_id
        return self

    def with_contact(self, phone: str | None = None, address: str | None = None,
                     emergency_contact: str | None = None) -> EmployeeBuilder:
        self._data.update(phone=phone, address=address, emergency_contact=emergency_contact)
        return self

    def with_equipment(self, laptop: bool = False, parking: bool = False) -> EmployeeBuilder:
        self._data.update(has_laptop=laptop, has_parking=parking)
        return self

    def with_access(self, vpn: bool = False, admin: bool = False) -> EmployeeBuilder:
        self._data.update(has_vpn_access=vpn, has_admin_rights=admin)
        return self

    def at_office(self, office_location: str) -> EmployeeBuilder:
        self._data["office_location"] = office_location
        return self

    def with_contract(self, contract_type: str) -> EmployeeBuilder:
        self._data["contract_type"] = contract_type
        return self

    def build(self) -> Employee:
        # All validation in one place, before the object exists
        d = self._data
        if not d.get("first_name") or not d.get("last_name"):
            raise ValueError("Name is required")
        if "@" not in d.get("email", ""):
            raise ValueError("Valid email is required")
        if "department" not in d:
            raise ValueError("Job information is required (with_job)")
        if d["salary"] < 0:
            raise ValueError("Salary cannot be negative")
        return Employee(**d)


# Presets: the "hidden logic" (a developer always gets laptop + VPN + admin)
# is now written once instead of remembered at every call.
class DeveloperBuilder(EmployeeBuilder):
    def __init__(self, first_name: str, last_name: str, email: str) -> None:
        super().__init__()
        (self.with_name(first_name, last_name)
             .with_email(email)
             .with_job("Engineering", "Senior Developer", 75000)
             .with_equipment(laptop=True)
             .with_access(vpn=True, admin=True)
             .at_office("Paris HQ"))


class InternBuilder(EmployeeBuilder):
    def __init__(self, first_name: str, last_name: str, email: str, department: str) -> None:
        super().__init__()
        (self.with_name(first_name, last_name)
             .with_email(email)
             .with_job(department, "Intern", 15000)
             .with_equipment(laptop=True)
             .at_office("Paris HQ")
             .with_contract("internship"))


if __name__ == "__main__":
    employee = (
        EmployeeBuilder()
        .with_name("John", "Doe")
        .with_email("john.doe@company.com")
        .with_job("Engineering", "Senior Developer", 75000)
        .starting_on("2024-01-15")
        .with_contact(phone="+33612345678")
        .with_equipment(laptop=True, parking=False)
        .with_access(vpn=True, admin=True)
        .at_office("Paris HQ")
        .build()
    )
    print(employee)

    dev = DeveloperBuilder("John", "Doe", "john.doe@company.com").build()
    intern = (InternBuilder("Jane", "Smith", "jane.smith@company.com", "Marketing")
              .with_manager(42).starting_on("2024-02-01").build())
    print(dev)
    print(intern)
