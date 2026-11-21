# UML Exo 2 - ABCD Records 📼

Statement: https://gist.github.com/bdallard/2d2407c4de4c182afca6d3ec7235e9eb

> Mermaid has no native use-case diagram, so use cases are drawn as rounded nodes
> inside a `subgraph` that plays the role of the system boundary.

## Level 1

### Task 1.1 - Use case diagram

```mermaid
flowchart LR
    M["🧍 Member"]
    C["🧍 Order Processing Clerk"]
    subgraph ABCD["ABCD Records system"]
        PO(["Place Order"])
        VM(["Verify Membership"])
        PR(["Process Order"])
        MP(["Make Payment"])
    end
    M --- PO
    M --- MP
    C --- VM
    C --- PR
```

### Task 1.2 - Class diagram

```mermaid
classDiagram
    class Member {
        -member_id: str
        -name: str
        -address: str
        -phone: str
        +place_order(items) Order
        +make_payment(order, payment)
    }
    class Order {
        -order_id: str
        -date: date
        -status: str
        -total: float
        +add_item(item, qty)
        +compute_total() float
    }
    class OrderProcessingClerk {
        -clerk_id: str
        -name: str
        +verify_membership(member) bool
        +process_order(order)
        +save_to_daily_file(order)
    }
    Member "1" -- "0..*" Order : places
    OrderProcessingClerk "1" -- "0..*" Order : processes
```

## Level 2

### Task 2.1 - Complete use case diagram

```mermaid
flowchart LR
    M["🧍 Member"]
    R["🧍 Royal Member"]
    N["🧍 Non-Member"]
    OC["🧍 Order Processing Clerk"]
    CC["🧍 Collection Dept. Clerk"]

    subgraph ABCD["ABCD Records system"]
        PO(["Place Order"])
        VM(["Verify Membership"])
        VA(["Verify Item Availability"])
        PR(["Process Order"])
        AD(["Apply Discount"])
        PI(["Print Invoice"])
        PS(["Print Shipping List"])
        OU(["Order Unavailable Items"])
        MP(["Make Payment"])
        SA(["Send Membership Application"])
    end

    R -. "is a" .-> M
    M --- PO
    M --- MP
    R --- OU
    N --- PO
    OC --- PR
    OC --- VM
    CC --- MP

    PO -. "«include»" .-> VM
    PR -. "«include»" .-> VA
    PR -. "«include»" .-> PI
    PR -. "«include»" .-> PS
    AD -. "«extend» (Royal member)" .-> PR
    OU -. "«extend» (item unavailable, Royal)" .-> PO
    SA -. "«extend» (not a member)" .-> VM
```

- **«include»**: always happens. Every order is checked for membership; every
  processed order checks availability and prints an invoice and a shipping list.
- **«extend»**: only under a condition. Discount only for Royal members, ordering
  unavailable items only for Royal members, and the application form only when
  the person is not a member.

### Task 2.2 - Complete class diagram

```mermaid
classDiagram
    class Member {
        <<abstract>>
        -member_id: str
        -name: str
        -address: str
        +place_order() Order
        +discount_rate()* float
        +can_order_unavailable()* bool
    }
    class RoyalMember {
        +discount_rate() float
        +can_order_unavailable() bool
        -priority: bool
    }
    class RegularMember {
        +discount_rate() float
        +can_order_unavailable() bool
    }
    class NonMember {
        -name: str
        -address: str
        +request_application() MembershipApplication
    }
    class MembershipApplication {
        -application_id: str
        -sent_date: date
        -status: str
    }
    class Order {
        -order_id: str
        -date: date
        -status: str
        +total() float
    }
    class OrderLine {
        -quantity: int
        -unit_price: float
        -backordered: bool
        +subtotal() float
    }
    class Item {
        <<abstract>>
        -code: str
        -title: str
        -artist: str
        -price: float
        -stock: int
        +is_available(qty) bool
    }
    class CD {
        -nb_tracks: int
    }
    class Tape {
        -duration_min: int
    }
    class Invoice {
        -invoice_id: str
        -amount: float
        -discount: float
        +print()
    }
    class ShippingList {
        -list_id: str
        -address: str
        +print()
    }
    class Payment {
        <<abstract>>
        -amount: float
        -date: date
        +process()* bool
    }
    class Cash
    class Check {
        -check_number: str
        -bank: str
    }
    class BankDraft {
        -draft_number: str
    }
    class OrderProcessingClerk {
        +verify_membership(person) bool
        +process_order(order)
    }
    class CollectionDeptClerk {
        +record_payment(payment)
    }
    class DailyRecordsFile {
        -date: date
        +save(order)
    }

    Member <|-- RoyalMember
    Member <|-- RegularMember
    Item <|-- CD
    Item <|-- Tape
    Payment <|-- Cash
    Payment <|-- Check
    Payment <|-- BankDraft

    Member "1" -- "0..*" Order : places
    NonMember "1" -- "0..1" MembershipApplication : receives
    Order "1" *-- "1..*" OrderLine
    OrderLine "0..*" --> "1" Item
    Order "1" -- "1" Invoice
    Order "1" -- "1" ShippingList
    Order "1" -- "0..1" Payment : paid by
    OrderProcessingClerk "1" -- "0..*" Order : processes
    CollectionDeptClerk "1" -- "0..*" Payment : records
    DailyRecordsFile "1" o-- "0..*" Order : stores
```

### Scenario - Royal member orders 2 CDs (one unavailable), pays by check

Object diagram of the state after the order is processed:

```mermaid
classDiagram
    class `marie : RoyalMember` {
        member_id = "R-042"
        name = "Marie"
    }
    class `o1 : Order` {
        order_id = "O-1001"
        status = "partially shipped"
    }
    class `l1 : OrderLine` {
        quantity = 1
        unit_price = 15.00
        backordered = false
    }
    class `l2 : OrderLine` {
        quantity = 1
        unit_price = 12.00
        backordered = true
    }
    class `cd1 : CD` {
        title = "Abbey Road"
        stock = 8
    }
    class `cd2 : CD` {
        title = "Kind of Blue"
        stock = 0
    }
    class `inv : Invoice` {
        amount = 24.30
        discount = 2.70
    }
    class `chk : Check` {
        amount = 24.30
        check_number = "0034567"
    }
    `marie : RoyalMember` -- `o1 : Order`
    `o1 : Order` *-- `l1 : OrderLine`
    `o1 : Order` *-- `l2 : OrderLine`
    `l1 : OrderLine` --> `cd1 : CD`
    `l2 : OrderLine` --> `cd2 : CD`
    `o1 : Order` -- `inv : Invoice`
    `o1 : Order` -- `chk : Check`
```

27.00€ of CDs minus the 10% Royal discount = **24.30€**. `cd2` is out of stock, but
Marie is Royal, so the line is kept as *backordered* instead of being refused.

## Level 3 - Sequence diagrams

### 1. Complete order processing flow

```mermaid
sequenceDiagram
    actor M as Member
    participant OC as OrderProcessingClerk
    participant O as Order
    participant I as Item
    participant F as DailyRecordsFile
    actor CC as CollectionDeptClerk

    M->>OC: place_order(items)
    OC->>OC: verify_membership(M)
    OC->>O: create(member)
    loop for each requested item
        OC->>I: is_available(qty)
        I-->>OC: true / false
        OC->>O: add_line(item, qty, backordered)
    end
    OC->>O: apply_discount(member.discount_rate())
    OC->>O: print_invoice()
    OC->>O: print_shipping_list()
    OC->>F: save(order)
    O-->>M: invoice + shipment
    M->>CC: payment
    CC->>CC: record_payment(payment)
```

### 2. Membership verification (success and failure)

```mermaid
sequenceDiagram
    actor P as Person
    participant OC as OrderProcessingClerk
    participant DB as MemberRegistry

    P->>OC: place_order(member_id, items)
    OC->>DB: find(member_id)
    alt member found
        DB-->>OC: member
        OC-->>P: order accepted, processing continues
    else not a member
        DB-->>OC: null
        OC->>OC: create MembershipApplication
        OC-->>P: order refused + membership application form
    end
```

### 3. Payment processing (all types)

```mermaid
sequenceDiagram
    actor M as Member
    participant CC as CollectionDeptClerk
    participant Pay as Payment
    participant B as Bank

    M->>CC: pay(invoice, method)
    alt Cash
        CC->>Pay: new Cash(amount)
        Pay-->>CC: accepted immediately
    else Check
        CC->>Pay: new Check(amount, number, bank)
        Pay->>B: clear check
        B-->>Pay: cleared / bounced
    else Bank draft
        CC->>Pay: new BankDraft(amount, number)
        Pay->>B: verify draft
        B-->>Pay: valid / invalid
    end
    alt accepted
        CC->>CC: mark invoice PAID
        CC-->>M: receipt
    else refused
        CC-->>M: payment refused, invoice still due
    end
```

### 4. Item reordering for Royal members

```mermaid
sequenceDiagram
    actor R as RoyalMember
    participant OC as OrderProcessingClerk
    participant I as Item
    participant S as Supplier

    R->>OC: place_order(cd2)
    OC->>I: is_available(1)
    I-->>OC: false
    OC->>R: can_order_unavailable()?
    alt Royal member
        R-->>OC: true
        OC->>S: reorder(cd2, qty)
        OC->>OC: line.backordered = true
        S-->>I: delivery, stock updated
        OC-->>R: ship cd2 (priority)
    else Regular member
        OC-->>R: item unavailable, line removed
    end
```
