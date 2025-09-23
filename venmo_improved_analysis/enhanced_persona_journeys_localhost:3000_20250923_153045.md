# Persona Journeys for http://localhost:3000

*Generated on: 2025-09-23 15:32:21*

```mermaid
sequenceDiagram
    participant W as Website
    participant U1 as New Customer
    participant U2 as Returning Customer
    participant U3 as Guest User
    participant U4 as Administrator
    participant U5 as Mobile User

    Note over U1: New Customer Journey
    U1->>+W: Step 1: observe
    W-->>-U1: Success
    Note right of U1: Feels: interested, satisfied, frustrated, motivated, confused

    Note over U2: Returning Customer Journey
    U2->>+W: Step 1: observe
    W-->>-U2: Success
    Note right of U2: Feels: interested, satisfied, frustrated, motivated, confused

    Note over U3: Guest User Journey
    U3->>+W: Step 1: observe
    W-->>-U3: Success
    Note right of U3: Feels: interested, satisfied, frustrated, motivated, confused

    Note over U4: Administrator Journey
    U4->>+W: Step 1: observe
    W-->>-U4: Success
    Note right of U4: Feels: interested, satisfied, motivated

    Note over U5: Mobile User Journey
    U5->>+W: Step 1: observe
    W-->>-U5: Success
    Note right of U5: Feels: interested, satisfied, motivated

```
