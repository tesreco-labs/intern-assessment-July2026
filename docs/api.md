# API Reference

The API is served by the Flask app in `app.py`. Start the app with `python app.py` before using these endpoints.

## Interns

### Register intern

`POST /register`

Request body:

```json
{
  "name": "Vaibhav",
  "email": "vaibhav@example.com",
  "domain": "Data Science",
  "duration": 3
}
```

Successful response: `201 Created`

```json
{
  "id": 1,
  "message": "Intern registered successfully"
}
```

### List interns

`GET /interns`

Returns an array of intern records ordered by newest first.

### Update intern

`PUT /intern/<id>`

Request body:

```json
{
  "name": "Vaibhav Kumar",
  "email": "vaibhav.kumar@example.com",
  "domain": "AI/ML",
  "duration": 6
}
```

### Delete intern

`DELETE /intern/<id>`

Deletes an intern. Attendance and mentor-assignment rows referencing that intern are removed through SQLite cascade rules.

## Attendance

### Add attendance

`POST /attendance`

Request body:

```json
{
  "intern_id": 1,
  "date": "2026-07-28",
  "status": "Present"
}
```

### List attendance

`GET /attendance`

Returns attendance rows with intern names joined from the `interns` table.

## Mentors

### Add mentor

`POST /mentor`

Request body:

```json
{
  "name": "Rahul Sharma",
  "specialization": "Machine Learning"
}
```

### List mentors

`GET /mentors`

Returns mentor rows ordered by newest first.

## Assignments

### Assign mentor

`POST /assign-mentor`

Request body:

```json
{
  "intern_id": 1,
  "mentor_id": 1
}
```

### List assignments

`GET /assignments`

Returns assignment rows with intern name, mentor name, and mentor specialization.
