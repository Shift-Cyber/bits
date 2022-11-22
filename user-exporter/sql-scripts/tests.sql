use hack_a_bit;

SELECT * from users;

# clear a user's discord id
UPDATE users SET discord_id = null WHERE email = "user@shiftcyber.com";