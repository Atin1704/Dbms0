# Event Management System API Documentation

## Authentication Endpoints

### 1. User Signup
- **URL**: `/signup/`
- **Method**: POST
- **Description**: Creates a new user account
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string",
    "confirmPassword": "string",
    "firstName": "string",
    "lastName": "string",
    "emailID": "string",
    "contactNo": "string"
  }
  ```

### 2. User Login
- **URL**: `/login/`
- **Method**: POST
- **Description**: Authenticates a user
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

### 3. Admin Login
- **URL**: `/admin/login/`
- **Method**: POST
- **Description**: Authenticates an admin
- **Request Body**:
  ```json
  {
    "emailID": "string",
    "password": "string"
  }
  ```

### 4. Organizer Login
- **URL**: `/organizer/login/`
- **Method**: POST
- **Description**: Authenticates an organizer
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

### 5. Organizer Signup
- **URL**: `/organizer/signup/`
- **Method**: POST
- **Description**: Creates a new organizer account
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string",
    "confirm_password": "string",
    "firstName": "string",
    "lastName": "string",
    "emailID": "string",
    "contactNo": "string"
  }
  ```

## Event Management Endpoints

### 6. Event Details
- **URL**: `/event/<int:event_id>/`
- **Method**: GET
- **Description**: Retrieves details of a specific event
- **URL Parameters**:
  - `event_id`: Integer ID of the event

### 7. Filtered Events
- **URL**: `/events/filtered/`
- **Method**: GET
- **Description**: Retrieves filtered events based on category
- **Query Parameters**:
  - `filter`: Category filter (ea, bt, fl, si, sf)
    - ea: Entertainment & Arts (Concert, Dance, Art)
    - bt: Business & Tech
    - fl: Food & Lifestyle
    - si: Social Impact
    - sf: Sports & Fitness

### 8. Events by Organizer
- **URL**: `/events/organizer/<int:organizer_id>/`
- **Method**: GET
- **Description**: Retrieves events organized by a specific organizer
- **URL Parameters**:
  - `organizer_id`: Integer ID of the organizer
- **Query Parameters**:
  - `filter`: 
    - 0: Upcoming events
    - 1: Past events

### 9. Organizer Average Rating
- **URL**: `/organizer/<int:organizer_id>/average-rating/`
- **Method**: GET
- **Description**: Retrieves average rating for an organizer
- **URL Parameters**:
  - `organizer_id`: Integer ID of the organizer

### 10. Organizer Complaints
- **URL**: `/organizer/<int:organizer_id>/complaints/`
- **Method**: GET
- **Description**: Retrieves complaint count for an organizer
- **URL Parameters**:
  - `organizer_id`: Integer ID of the organizer
- **Query Parameters**:
  - `event_id`: Optional event ID to filter complaints

## User Management Endpoints

### 11. User Details
- **URL**: `/user/<int:id>/`
- **Method**: GET
- **Description**: Retrieves details of a specific user
- **URL Parameters**:
  - `id`: Integer ID of the user

### 12. Admin Details
- **URL**: `/admin/<int:id>/`
- **Method**: GET
- **Description**: Retrieves details of a specific admin
- **URL Parameters**:
  - `id`: Integer ID of the admin

### 13. Organizer Details
- **URL**: `/organizer/<int:id>/`
- **Method**: GET
- **Description**: Retrieves details of a specific organizer
- **URL Parameters**:
  - `id`: Integer ID of the organizer

### 14. Unverified Organizers
- **URL**: `/admin/unverified-organizers/`
- **Method**: GET
- **Description**: Lists all unverified organizers

### 15. Organizer Event Feedback
- **URL**: `/organizer/<int:organizer_id>/feedbacks/`
- **Method**: GET
- **Description**: Retrieves feedback for organizer's events
- **URL Parameters**:
  - `organizer_id`: Integer ID of the organizer
- **Query Parameters**:
  - `event_id`: Optional event ID to filter feedback

## Registration and Transactions

### 16. User Registration Transactions
- **URL**: `/user/<int:user_id>/registrations/`
- **Method**: GET
- **Description**: Retrieves registration transactions for a user
- **URL Parameters**:
  - `user_id`: Integer ID of the user

### 17. User Event List
- **URL**: `/user/<int:user_id>/events/`
- **Method**: GET
- **Description**: Retrieves events registered by a user
- **URL Parameters**:
  - `user_id`: Integer ID of the user
- **Query Parameters**:
  - `filter`: 
    - 1: Upcoming events
    - 2: Past events

### 18. Complaint Details
- **URL**: `/complaint/<int:complaint_id>/`
- **Method**: GET
- **Description**: Retrieves details of a specific complaint
- **URL Parameters**:
  - `complaint_id`: Integer ID of the complaint

### 19. Feedback Details
- **URL**: `/feedback/<int:feedback_id>/`
- **Method**: GET
- **Description**: Retrieves details of a specific feedback
- **URL Parameters**:
  - `feedback_id`: Integer ID of the feedback

### 20. Transaction Details
- **URL**: `/transaction/<int:transaction_id>/`
- **Method**: GET
- **Description**: Retrieves details of a specific transaction
- **URL Parameters**:
  - `transaction_id`: Integer ID of the transaction

### 21. Registration Details
- **URL**: `/api/registration/<int:registration_id>/`
- **Method**: GET
- **Description**: Retrieves details of a specific registration
- **URL Parameters**:
  - `registration_id`: Integer ID of the registration 