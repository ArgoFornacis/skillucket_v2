# Skill Management APIs

## 1. Get Categories

- **Endpoint**: `GET /api/categories/`
- **Purpose**: Get a list of all skill categories.

- **Response**:
  - Status: 200 OK
  - Body: A JSON response containing the serialized list of skill categories.

- **Usage Example**:
  Make a GET request to this endpoint to retrieve a list of all skill categories.

## 2. Get Skills by Category

- **Endpoint**: `GET /api/categories/{category_id}/skills/`
- **Purpose**: Get a list of skills within a specific category.

- **Parameters**:
  - `category_id` (integer): The ID of the category to filter skills.

- **Response**:
  - Status: 200 OK
  - Body: A JSON response containing the serialized list of skills in the specified category.

- **Usage Example**:
  Make a GET request to this endpoint, replacing `{category_id}` with the actual category ID, to retrieve a list of skills in that category.

## 3. Manage User Skills

- **Endpoint**: `POST /api/user_skills/` and `DELETE /api/user_skills/`
- **Purpose**: Add or remove a skill to/from the user's skill list.

### Payload:

```json
{
    "skill_id": 123
}

```

- **Methods**:
  - `POST`: Add a skill to the user's skills.
  - `DELETE`: Remove a skill from the user's skills.

- **Parameters**:
  - `skill_id` (integer): The ID of the skill to add or remove.

- **Response**:
  - Status: 201 Created (for `POST`), 204 No Content (for `DELETE`)
  - Body (for `POST`): A JSON response confirming the action.
  - Body (for `DELETE`): A JSON response confirming the removal.

- **Usage Example**:
  - Use `POST` to add a skill to the user's skills.
  - Use `DELETE` to remove a skill from the user's skills.

## 4. Manage Bucket Skills

- **Endpoint**: `POST /api/bucket_skills/` and `DELETE /api/bucket_skills/`
- **Purpose**: Add or remove a skill to/from the user's bucket list.

### Payload:

```json
{
    "skill_id": 456
}

```

- **Methods**:
  - `POST`: Add a skill to the user's bucket list.
  - `DELETE`: Remove a skill from the user's bucket list.

- **Parameters**:
  - `skill_id` (integer): The ID of the skill to add or remove.

- **Response**:
  - Status: 201 Created (for `POST`), 204 No Content (for `DELETE`)
  - Body (for `POST`): A JSON response confirming the action.
  - Body (for `DELETE`): A JSON response confirming the removal.

- **Usage Example**:
  - Use `POST` to add a skill to the user's bucket list.
  - Use `DELETE` to remove a skill from the user's bucket list.

## 5. Get User Skills

- **Endpoint**: `GET /api/user_skills_list/`
- **Purpose**: Get a list of the user's current skills.

- **Response**:
  - Status: 200 OK
  - Body: A JSON response containing the serialized list of user's current skills.

- **Usage Example**:
  Make a GET request to this endpoint to retrieve a list of the user's current skills.

## 6. Get Bucket Skills

- **Endpoint**: `GET /api/bucket_skills_list/`
- **Purpose**: Get a list of the user's current bucket list skills.

- **Response**:
  - Status: 200 OK
  - Body: A JSON response containing the serialized list of user's current bucket list skills.

- **Usage Example**:
  Make a GET request to this endpoint to retrieve a list of the user's current bucket list skills.

## 7. User Skill Detail

- **Endpoint**: `GET /api/user_skills/{user_skill_id}/`, `PUT /api/user_skills/{user_skill_id}/`, and `PATCH /api/user_skills/{user_skill_id}/`
- **Purpose**: Retrieve or update user skill details.

### Payload:

```json
{
    "skill_id": 789,
    "proficiency_level": "Intermediate"
}

```

- **Methods**:
  - `GET`: Retrieve user skill details.
  - `PUT` and `PATCH`: Update user skill details.

- **Parameters**:
  - `user_skill_id` (integer): The ID of the user skill to retrieve or update.

- **Response**:
  - Status: 200 OK (for `GET`), 200 OK (for `PUT` and `PATCH`)
  - Body (for `GET`): A JSON response containing the user skill details.
  - Body (for `PUT` and `PATCH`): A JSON response confirming the update or providing validation errors.

- **Usage Example**:
  - Use `GET` to retrieve user skill details.
  - Use `PUT` or `PATCH` to update user skill details.

## 8. Bucket Skill Detail

- **Endpoint**: `GET /api/bucket_skills/{bucket_skill_id}/`, `PUT /api/bucket_skills/{bucket_skill_id}/`, and `PATCH /api/bucket_skills/{bucket_skill_id}/`
- **Purpose**: Retrieve or update bucket skill details.

### Payload:

```json
{
    "skill_id": 1011,
    "target_date": "2024-12-31"
}

```

- **Methods**:
  - `GET`: Retrieve bucket skill details.
  - `PUT` and `PATCH`: Update bucket skill details.

- **Parameters**:
  - `bucket_skill_id` (integer): The ID of the bucket skill to retrieve or update.

- **Response**:
  - Status: 200 OK (for `GET`), 200 OK (for `PUT` and `PATCH`)
  - Body (for `GET`): A JSON response containing the bucket skill details.
  - Body (for `PUT` and `PATCH`): A JSON response confirming the update or providing validation errors.

- **Usage Example**:
  - Use `GET` to retrieve bucket skill details.
  - Use `PUT` or `PATCH` to update bucket skill details.
