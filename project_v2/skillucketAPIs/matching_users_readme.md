# User Matching APIs



## 1. List All Matches for a User

- **Endpoint**: `GET /api/matches/`
- **Purpose**: Retrieve users who can teach skills you want to learn.

### Response:
A list of user profiles that match your learning goals (bucket_skill).

### Usage Example:
Simply make a GET request to this endpoint to find users who possess the skills you've added to your learning bucket list.

---

## 2. Search Users by Skill

- **Endpoint**: `GET /api/search_skill/?name=<skill_name>`
- **Purpose**: Search for users based on a specific skill.

### Response:
A list of users who have the queried skill.

### Usage Example:
To find users who know "Python", use the URL `/api/search_skill/?name=python`. This will return a list of users who have "Python" as one of their skills.
The skill name is case-insensitive and works with partial string.
