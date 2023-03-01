templates = {1: "SELECT logging, logging_type, logging_stage FROM states WHERE telegram_id = {}",
             2: "SELECT age_wish, city_wish, sex_wish FROM users_info WHERE telegram_id = {}",
             3: "UPDATE states SET logging=False, logging_type=0, logging_stage=0 WHERE telegram_id={};",
             4: "UPDATE states SET logging=True, logging_type={}, logging_stage={} WHERE telegram_id={};",
             5: "INSERT INTO photos VALUES ({}, '{}');",
             6: "UPDATE photos SET photo_id='{}' WHERE telegram_id={}",
             7: "INSERT INTO users VALUES ({}, '{}', '{}', '{}', '{}', 'en');",
             8: "INSERT INTO states VALUES ({}, {}, {}, {}, {});",
             9: "INSERT INTO users_info VALUES ({});",
             10: "UPDATE users_info SET {}={} WHERE telegram_id={};",
             11: "UPDATE users_info SET age_wish='{}'::int4range WHERE telegram_id={};",
             12: "SELECT * FROM users_info WHERE age_wish={} AND city_wish={} AND sex_wish={}",
             13: "INSERT INTO cities VALUES ('{}', '{}', {})",
             14: "INSERT INTO main_messages VALUES ({}, {}, {})",
             15: "DELETE FROM main_messages WHERE telegram_id={} AND message_type={}",
             16: "SELECT message_id FROM main_messages WHERE telegram_id={} AND message_type={}",
             17: "SELECT * FROM cities ORDER BY population DESC;",
             18: "SELECT users_info.telegram_id, users_info.age, users_info.city, users_info.sex, "
                 "users_searching_buffer.specified, users_searching_buffer.buffering_time FROM users_info "
                 "INNER JOIN users_searching_buffer ON " 
                 "users_searching_buffer.telegram_id = users_info.telegram_id AND '{}'::int4range @> "
                 "age::integer AND city='{}' AND sex={} AND users_info.telegram_id != {} AND specified = true "
                 "ORDER BY users_searching_buffer.buffering_time DESC "
                 "LIMIT 1;",
             19: "SELECT * FROM {} WHERE telegram_id = {};",
             20: "DELETE FROM {} WHERE telegram_id = {};",
             21: "UPDATE users SET language='{}' WHERE telegram_id={};",
             22: "SELECT city FROM cities WHERE city LIKE '{}%' ORDER BY population DESC LIMIT {}",
             23: "SELECT on_chatting FROM states WHERE telegram_id = {};",
             24: "UPDATE states SET on_chatting = {} WHERE telegram_id = {};",
             25: "SELECT users_info.telegram_id, "
                 "users_info.age, users_info.city, users_info.sex, users_searching_buffer.specified, "
                 "users_searching_buffer.buffering_time "
                 "FROM users_info "
                 "INNER JOIN users_searching_buffer ON "
                 "users_searching_buffer.telegram_id = users_info.telegram_id AND users_info.telegram_id != {} AND NOT specified "
                 "ORDER BY users_searching_buffer.buffering_time DESC "
                 "LIMIT 1;",
             26: "DELETE FROM users_searching_buffer WHERE telegram_id={};",
             27: "INSERT INTO users_searching_buffer VALUES ({}, '{}', {});"
             }
