-- SQLite
SELECT * FROM course_attendance WHERE created_at == "2023-11-15"

SELECT * FROM course_attendance;


UPDATE course_attendance
SET created_at = '2023-11-17'  -- Use the specific time of day as needed
WHERE batch_id = 1 AND id= 92;

SELECT * FROM authentication_user

SELECT * FROM course_batch

SELECT * FROM authentication_user