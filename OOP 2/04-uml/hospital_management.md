# UML Exo 1 - Hospital Management System 🏥

Statement: https://gist.github.com/bdallard/2d2407c4de4c182afca6d3ec7235e9eb
Implementation of the final design: [`hospital.py`](hospital.py)

## Task 1 - Basic class diagram

```mermaid
classDiagram
    class Patient {
        -patient_id: str
        -name: str
        -password: str
        -email: str
        +post_problem(description) HealthProblem
        +receive_prescription(prescription)
        +pay(amount, method)
    }
    class Organizer {
        -organizer_id: str
        -name: str
        -password: str
        +read_problem(problem)
        +consult_doctor(doctor, problem)
        +send_prescription(patient, prescription)
        +forward_payment(doctor, payment)
    }
    class Doctor {
        -doctor_id: str
        -name: str
        -password: str
        -speciality: str
        +review_problem(problem)
        +write_prescription(problem) Prescription
        +receive_payment(payment)
    }

    Patient "1..*" -- "1" Organizer : submits problems to >
    Organizer "1" -- "1..*" Doctor : consults >
    Doctor "1" -- "0..*" Patient : treats >
```

- An organizer handles many patients and consults many doctors.
- A doctor can treat zero or more patients; a patient deals with one organizer.

## Task 2 - Full class diagram (6 classes)

```mermaid
classDiagram
    class Patient {
        -patient_id: str
        -name: str
        -password: str
        +post_problem(description) HealthProblem
        +pay(prescription, method) Payment
    }
    class Doctor {
        -doctor_id: str
        -name: str
        -speciality: str
        +write_prescription(problem, text) Prescription
    }
    class Organizer {
        -organizer_id: str
        -name: str
        +consult_doctor(problem, doctor)
        +send_prescription(prescription)
        +forward_payment(payment)
    }
    class HealthProblem {
        -problem_id: str
        -description: str
        -submitted_at: datetime
    }
    class Prescription {
        -prescription_id: str
        -content: str
        -fee: float
    }
    class Payment {
        <<abstract>>
        -payment_id: str
        -amount: float
        -paid_at: datetime
        +process()* bool
    }
    class CheckPayment {
        -check_number: str
        +process() bool
    }
    class CashPayment {
        +process() bool
    }
    class CreditCardPayment {
        -card_last4: str
        +process() bool
    }

    Patient "1" *-- "0..*" HealthProblem : posts
    HealthProblem "1" -- "0..1" Prescription : answered by
    Doctor "1" -- "0..*" Prescription : writes
    Prescription "1" -- "0..1" Payment : paid by
    Payment <|-- CheckPayment
    Payment <|-- CashPayment
    Payment <|-- CreditCardPayment
    Organizer "1" -- "0..*" HealthProblem : manages
```

- **Composition** Patient ◆ HealthProblem: a problem has no meaning without its patient.
- **Inheritance** for payment types: each type has its own data (check number, card)
  and its own `process()`.

### Sequence diagram - submit a problem, get a prescription, pay

```mermaid
sequenceDiagram
    actor P as Patient
    participant O as Organizer
    participant D as Doctor

    P->>O: post_problem(description)
    O->>O: read_problem()
    O->>D: consult_doctor(problem)
    D-->>O: write_prescription(problem)
    O-->>P: send_prescription(prescription)
    P->>O: pay(prescription, CreditCard)
    O->>O: payment.process()
    O->>D: forward_payment(payment)
    D-->>O: ack
    O-->>P: receipt
```

## Task 3 - Advanced design

```mermaid
classDiagram
    class User {
        <<abstract>>
        #user_id: str
        #name: str
        #password_hash: str
        +login(password) bool
        +logout()
    }
    class Patient {
        -history: list~Prescription~
        +post_problem(description) HealthProblem
        +pay(prescription, method) Payment
        +past_prescriptions() list
    }
    class Doctor {
        -speciality: str
        +write_prescription(problem, content, fee) Prescription
    }
    class Organizer {
        +register_member(role, name, password) User
        +assign(problem, doctor)
        +deliver(prescription)
        +forward_payment(payment)
    }
    class ProblemStatus {
        <<enumeration>>
        PENDING
        IN_REVIEW
        RESOLVED
    }
    class HealthProblem {
        -problem_id: str
        -description: str
        -status: ProblemStatus
        -created_at: datetime
        -updated_at: datetime
        +set_status(status)
    }
    class Prescription {
        -prescription_id: str
        -content: str
        -fee: float
        -issued_at: datetime
        -based_on: Prescription
    }
    class Payment {
        -amount: float
        -status: str
        -paid_at: datetime
        -method: PaymentMethod
        +execute() bool
    }
    class PaymentMethod {
        <<interface>>
        +pay(amount) bool
    }
    class CheckMethod
    class CashMethod
    class CreditCardMethod

    User <|-- Patient
    User <|-- Doctor
    User <|-- Organizer
    Patient "1" *-- "0..*" HealthProblem
    HealthProblem --> ProblemStatus
    HealthProblem "0..*" --> "0..1" Doctor : assigned to
    HealthProblem "1" -- "0..1" Prescription
    Prescription "0..*" --> "0..1" Prescription : based_on (renewal)
    Doctor "1" -- "0..*" Prescription : writes
    Prescription "1" -- "0..1" Payment
    Payment o-- PaymentMethod : strategy
    PaymentMethod <|.. CheckMethod
    PaymentMethod <|.. CashMethod
    PaymentMethod <|.. CreditCardMethod
```

### SSD 1 - Patient registration

```mermaid
sequenceDiagram
    actor O as Organizer
    participant S as :System
    O->>S: register_member("patient", name)
    S->>S: generate member_id + temporary password
    S-->>O: member_id, password
    O-->>O: sends credentials to the new patient
```

### SSD 2 - Consultation flow

```mermaid
sequenceDiagram
    actor P as Patient
    participant S as :System
    actor O as Organizer
    actor D as Doctor
    P->>S: login(id, password)
    P->>S: post_problem(description)
    S-->>P: problem_id (status = PENDING)
    O->>S: assign(problem_id, doctor_id)
    S-->>S: status = IN_REVIEW
    D->>S: write_prescription(problem_id, content, fee)
    O->>S: deliver(prescription_id)
    S-->>S: status = RESOLVED
    S-->>P: prescription available
```

### SSD 3 - Payment processing

```mermaid
sequenceDiagram
    actor P as Patient
    participant S as :System
    actor O as Organizer
    actor D as Doctor
    P->>S: pay(prescription_id, method)
    S->>S: method.pay(amount)
    alt payment accepted
        S-->>P: receipt (status = PAID)
        O->>S: forward_payment(payment_id)
        S-->>D: amount credited (status = FORWARDED)
    else refused
        S-->>P: error, prescription still unpaid
    end
```

## Questions to consider

1. **Multiple doctors per patient?** The link is through `HealthProblem`: each
   problem is assigned to one doctor, so a patient with several problems can see
   several doctors (Patient 1 → * HealthProblem * → 0..1 Doctor). For a second
   opinion on the *same* problem, make the assignment a `Consultation` association
   class (problem, doctor, date, notes), giving HealthProblem 1 → * Consultation.
2. **Reusable prescriptions?** Yes for renewals: a new `Prescription` points to the
   one it is `based_on`, so the history is kept and each renewal has its own date
   and fee. The patient's `past_prescriptions()` gives the doctor that history.
3. **Design pattern for payments?** **Strategy**: `Payment` holds a
   `PaymentMethod` interface and calls `pay()` without knowing if it is check,
   cash or card. A new method (e.g. Apple Pay) is a new class, with no change to
   `Payment` (Open/Closed). A Factory can create the right method from a string.
4. **Data integrity during payment?** Treat a payment as a transaction with
   explicit states (PENDING → PAID → FORWARDED): the amount must equal the
   prescription fee, a prescription can be paid only once, forwarding is allowed
   only after PAID, and every step is timestamped. In a real system these updates
   are done in one database transaction so a crash never leaves "paid but not
   recorded".
