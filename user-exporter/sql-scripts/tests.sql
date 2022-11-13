use hack_a_bit;

SELECT * from users;

UPDATE users 
SET first_name = 'Michael', last_name = 'Pelletier', email = 'michael@neonremedystudios.com', registered = '0'
WHERE user_id = 1;
