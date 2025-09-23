# Goal Achievement for http://localhost:3000

*Generated on: 2025-09-23 15:32:21*

```mermaid
graph LR
    subgraph "Goal Achievement Matrix"
    P0["New Customer"]
    G0_0["❌ Find products"]
    P0["New Customer"] --> G0_0
    G0_1["❌ Make purchase"]
    P0["New Customer"] --> G0_1
    G0_2["❌ Create account"]
    P0["New Customer"] --> G0_2
    P1["Returning Customer"]
    G1_0["❌ Quick purchase"]
    P1["Returning Customer"] --> G1_0
    G1_1["❌ Check account"]
    P1["Returning Customer"] --> G1_1
    G1_2["❌ Reorder items"]
    P1["Returning Customer"] --> G1_2
    P2["Guest User"]
    G2_0["❌ Browse content"]
    P2["Guest User"] --> G2_0
    G2_1["❌ Get information"]
    P2["Guest User"] --> G2_1
    G2_2["❌ Avoid registration"]
    P2["Guest User"] --> G2_2
    P3["Administrator"]
    G3_0["❌ Manage content"]
    P3["Administrator"] --> G3_0
    G3_1["❌ Monitor users"]
    P3["Administrator"] --> G3_1
    G3_2["❌ System maintenance"]
    P3["Administrator"] --> G3_2
    P4["Mobile User"]
    G4_0["❌ Quick browsing"]
    P4["Mobile User"] --> G4_0
    G4_1["❌ Easy checkout"]
    P4["Mobile User"] --> G4_1
    G4_2["❌ Touch-friendly interface"]
    P4["Mobile User"] --> G4_2
    end

    classDef achieved fill:#4CAF50,stroke:#333,stroke-width:2px,color:#fff
    classDef not_achieved fill:#f44336,stroke:#333,stroke-width:2px,color:#fff
    classDef persona fill:#2196F3,stroke:#333,stroke-width:3px,color:#fff
```
