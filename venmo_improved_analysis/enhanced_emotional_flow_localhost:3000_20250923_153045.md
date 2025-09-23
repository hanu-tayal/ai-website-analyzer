# Emotional Flow for http://localhost:3000

*Generated on: 2025-09-23 15:32:21*

```mermaid
flowchart TD
    subgraph "Emotional User Journey"
    S0["🚀 New Customer<br/>Starts Journey"]
    N0_0["✅ observe<br/>(content)<br/>interested, satisfied"]
    S0 --> N0_0
    E0["🚫 Journey<br/>Abandoned"]
    N0_0 --> E0
    S1["🚀 Returning Customer<br/>Starts Journey"]
    N1_0["✅ observe<br/>(content)<br/>interested, satisfied"]
    S1 --> N1_0
    E1["🚫 Journey<br/>Abandoned"]
    N1_0 --> E1
    S2["🚀 Guest User<br/>Starts Journey"]
    N2_0["✅ observe<br/>(content)<br/>interested, satisfied"]
    S2 --> N2_0
    E2["🚫 Journey<br/>Abandoned"]
    N2_0 --> E2
    S3["🚀 Administrator<br/>Starts Journey"]
    N3_0["✅ observe<br/>(content)<br/>interested, satisfied"]
    S3 --> N3_0
    E3["🚫 Journey<br/>Abandoned"]
    N3_0 --> E3
    S4["🚀 Mobile User<br/>Starts Journey"]
    N4_0["✅ observe<br/>(content)<br/>interested, satisfied"]
    S4 --> N4_0
    E4["🚫 Journey<br/>Abandoned"]
    N4_0 --> E4
    end

    classDef success fill:#4CAF50,stroke:#333,stroke-width:2px,color:#fff
    classDef failure fill:#f44336,stroke:#333,stroke-width:2px,color:#fff
    classDef neutral fill:#9E9E9E,stroke:#333,stroke-width:1px,color:#fff
```
