# User Management APIs

## 1. User Registration

- **Endpoint**: `POST /api/register/`
- **Purpose**: Register a new user.

### Payload:

```json
{
    "username": "your_username",
    "password": "your_password",
    "email": "your_email@example.com",
    "first_name": "John", (optional)
    "last_name": "Doe", (optional)
    "image": "base64_encoded_image_data" (optional)
}
```

- **Response**:
Confirmation of successful registration.

- **Usage Example**:
Use this endpoint to register a new user. Provide all required and optionally details.

  

## 2. User Login

- **Endpoint**: `POST /api/login/`
- **Purpose**: Login user and generate token.

### Payload:

```json
{
    "username": "your_username",
    "password": "your_password"
}
```

- **Response**:
Authentication token.

- **Usage Example**:
Use this endpoint to log in. Use the returned token in the headers of your subsequent requests to authenticate.

## 3. User Profile

- **Endpoint**: `GET /api/profile/`
- **Purpose**: Get the profile of the authenticated user.


- **Response**:
User's profile data.

- **Usage Example**:
Make a GET request to this endpoint after logging in to retrieve your profile information.


## 4. User Profile

- **Endpoint**: `PUT /api/profile/`
- **Purpose**: Update the authenticated user's profile.

### Payload:

```json{
    "username": "NewUsername",
    "first_name": "NewFirst",
    "last_name": "NewLast",
    "email": "new_email@example.com",
    "image": "new_base64_encoded_image_data"
}

```

- **Response**:
 New user's profile data.

- **Usage Example**:
Use this endpoint to update your profile information. Only provide the fields you want to update.


## 5. Change Password

- **Endpoint**: `PUT /api/change_password/`
- **Purpose**: Update the authenticated user's password.

### Payload:

```json
{
    "old_password": "your_old_password",
    "new_password": "your_new_password"
}


```

- **Response**:
Confirmation of successful password change.

- **Usage Example**:
If you wish to change your password, use this endpoint. Provide both your old password and the new one.

## 6. User Logout

- **Endpoint**: `POST /api/logout/`
- **Purpose**: Logout the user and delete his token from the database.

- **Response**:
Confirmation of successful logout.

- **Usage Example**:
Use this endpoint to logout from your session.