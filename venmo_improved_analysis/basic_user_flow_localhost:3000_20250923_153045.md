# User Flow Diagram for http://localhost:3000

*Generated on: 2025-09-23 15:32:21*

```mermaid
graph TD
    A[User visits website] --> B{Is user logged in?}
    B -->|No| C[Registration/Login page]
    B -->|Yes| D[User Dashboard]
    C --> E[Authentication]
    E --> D
    D --> J[Support/Help]
    D --> P[Search]

```
