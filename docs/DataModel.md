# Data Model Documentation

This document describes the database schema for the **Factory Machinery Status & Repair Tracking System**. It outlines each entity (table), key fields, and the relationships between them, providing a shared understanding of how data is structured and maintained.

---

## 1. Overview

- **Primary Entities**:  
  - `machinery`  
  - `fault_cases`  
  - `fault_notes`  
  - `warnings`  
  - `users`  
  - `collection` (plus the join table `machinery_collections`)  
  - `machinery_assignment` (to track if/when a machine is assigned)  

- **Relationship Highlights**:  
  - A single machine can have multiple fault cases, warnings, and collections.  
  - Users file and resolve faults or warnings (role-based actions).  
  - The assignment table can link machines to specific users (e.g., technicians, repair staff).

---

## 2. ERD(Entity Relationship Diagram)

Here’s our high-level ERD. For a larger view, see [the diagram on Imgur](https://imgur.com/f9IaWjw.png).

![ERD Diagram](https://imgur.com/f9IaWjw.png)

**Diagram Explanation**:  
- Each box represents a table (entity).  
- The lines show relationships (e.g., many-to-one from `fault_cases` to `machinery`).  
- PK = Primary Key, FK = Foreign Key.

---

## 3. Entities & Fields

### 3.1 Users
| Field       | Type     | Description                           |
|-------------|----------|---------------------------------------|
| **user_id** (PK) | bigint   | Unique ID for each user.          |
| **first_name**   | varchar  | Required |
| **last_name**    | varchar  | Required |
| **email**        | varchar  | Required |
| **password**     | varchar  | Required |
| **role**         | enum     | One of `MANAGER`, `TECHNICIAN`, `REPAIR`. |

### 3.2 Machinery
| Field          | Type     | Description                             |
|----------------|----------|-----------------------------------------|
| **machine_id** (PK) | bigint   | Unique machine identifier.              |
| **name**       | varchar  | Display name (e.g., “Conveyor Belt #2”).   |
| **model**      | varchar  | Optional field for machine’s model/type.   |
| **description**| varchar  | Longer text describing the machine.        |
| **status**     | enum     | `OK`, `WARNING`, or `FAULT`.               |
| **priority**   | int      | Higher number = more important.      |

### 3.3 Warnings
| Field         | Type     | Description                                     |
|---------------|----------|-------------------------------------------------|
| **warning_id** (PK) | bigint   | Unique warning identifier.                    |
| **is_active** | boolean | True if the warning is still relevant.            |
| **machine_id** (FK) | int  | Links to the `machinery` table.                |
| **message**   | text    | Description of the warning.                       |
| **added_by**  | int (FK)| The user who created this warning.                |
| **created_at**| timestamp | Timestamp it was created.                        |
| **resolved_by** | int (FK)| User who cleared the warning, if any.           |
| **resolved_at** | timestamp | When it was cleared.                           |

### 3.4 Fault Cases
| Field        | Type     | Description                                           |
|--------------|----------|-------------------------------------------------------|
| **case_id** (PK)   | bigint   | Unique fault case ID.                                |
| **machine_id** (FK)| int      | References `machinery`.                             |
| **created_by** (FK)| int      | The user who reported the fault.                    |
| **status**   | enum     | Could be `OPEN`, `RESOLVED`, etc.                        |
| **created_at**| timestamp | Fault creation time.                                   |
| **resolved_at**| timestamp | Time the fault was closed.                            |
| **resolved_by** (FK)| int  | User who resolved the fault (Repair or Manager).      |

### 3.5 Fault Notes
| Field        | Type     | Description                                  |
|--------------|----------|----------------------------------------------|
| **note_id** (PK) | bigint   | Unique ID for each note.                    |
| **case_id** (FK)| int       | Links to the `fault_cases` table.           |
| **user_id** (FK)| int       | The user who wrote the note.                |
| **note**     | text     | The note content.                             |
| **created_at**| timestamp | When the note was created.                   |

### 3.6 Collection
| Field            | Type     | Description                         |
|------------------|----------|-------------------------------------|
| **collection_id** (PK) | bigint   | Unique ID for each collection.        |
| **name**         | varchar  | A label for the collection (e.g., “Building-A”). |
| **description**  | varchar  | Optional longer text.                 |
| **created_at**   | timestamp| When this collection was added.       |

### 3.7 Machinery Collections (Join Table)
| Field             | Type | Description                                 |
|-------------------|------|---------------------------------------------|
| **mach_coll_id** (PK)| bigint| Unique record ID.                           |
| **collection_id** (FK)| int   | Points to `collection`.                  |
| **machinery_id** (FK)| int    | Points to `machinery`.                   |

*(Implements a many-to-many relationship between **machinery** and **collection**.)*

### 3.8 Machinery Assignment
| Field         | Type     | Description                                       |
|---------------|----------|---------------------------------------------------|
| **assignment_id** (PK) | bigint   | Unique record ID.                            |
| **is_active** | boolean | True if the assignment is currently valid.         |
| **assigned_at**| timestamp | Date/time of the assignment.                     |
| **machine_id** (FK) | int| Links to the `machinery` table.                   |
| **assigned_by** (FK)  | int| The manager who created the assignment.       |
| **assigned_to** (FK)  | int| The technician/repair who is assigned to the machine.       |


---

## 4. Relationship Details

1. **Machinery ↔ Collections**: Many-to-many via `machinery_collections`.  
2. **Machinery → Fault Cases**: One machine can have multiple faults.  
3. **Machinery → Warnings**: One machine can have multiple warnings.  
4. **Fault Cases → Fault Notes**: Each fault can have many notes.  
5. **User**: Linked to fault cases (created_by, resolved_by), warnings (added_by, resolved_by), and machine assignments(assigned_to, assigned_by).

---

## 5. Conclusion

This schema supports:
- **Machine** tracking with statuses and priorities.  
- **Faults** and **Warnings** tied to users.  
- **Role-based** logic for who can create or resolve.  
- **Collections** to group machines.  
- **Assignments** to link specific users to machines.

Keep this file updated whenever the schema evolves so it remains the **source of truth** for the project’s data model.