
CREATE TABLE user_info_table (
	user_id INT PRIMARY KEY,
	user_age INT NOT NULL,
	user_location VARCHAR(255) NOT NULL
);

CREATE TABLE user_description_table (
    user_id INT NOT NULL,
    user_description VARCHAR(255) NOT NULL,
    user_values VARCHAR(255) NOT NULL, --насчет этого хз, возможно будет легче предлагать ценности? тогда INT NOT NULL
    user_children INT,
    user_desc_children VARCHAR(255) NOT NULL, --возможно стоит добавить описание по типу (два сыночка)
    user_hobbies INT, --также, либо описание либо предлагать пользователю выбор условно из 10 хобби
    user_personal_traits VARCHAR(255) NOT NULL,
    user_target_life VARCHAR(255) NOT NULL
);

CREATE TABLE user_personality_data (
    user_id INT NOT NULL,
    user_login VARCHAR(255) NOT NULL,
    user_pwd VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL
);

CREATE TABLE user_favorites_likes (
    user_id INT NOT NULL,
    user_InFavorit_id INT NOT NULL,
    user_messages INT[3]
);

CREATE TABLE user_message (
    user_id_1 INT NOT NULL,
    user_id_2 INT NOT NULL,
    messages VARCHAR(255)[]
);

CREATE TABLE user_matches (
    user_id_1 INT NOT NULL,
    user_id_2 INT NOT NULL,
    user_matches INT[3]
);

INSERT INTO user_info_table (user_id, user_age, user_location) VALUES
(1, 25, 'Moscow'),
(2, 30, 'New York'),
(3, 28, 'London');

INSERT INTO user_description_table (user_id, user_description, user_values, user_children, user_desc_children, user_hobbies, user_personal_traits, user_target_life) VALUES
(1, 'Любит путешествия', 'Доброта', 0, 'Нет детей', 1, 'Энергичный', 'Стать разработчиком'),
(2, 'Фотограф', 'Творчество', 2, 'Двое детей', 3, 'Креативный', 'Открыть выставку'),
(3, 'Учитель', 'Образование', 1, 'Один ребенок', 2, 'Терпеливый', 'Написать книгу');

INSERT INTO user_personality_data (user_id, user_login, user_pwd, user_email) VALUES
(1, 'user1', 'pass1', 'email1@test.com'),
(2, 'user2', 'pass2', 'email2@test.com'),
(3, 'user3', 'pass3', 'email3@test.com');

INSERT INTO user_favorites_likes (user_id, user_InFavorit_id, user_messages) VALUES
(1, 2, ARRAY[1,2,3]),
(2, 1, ARRAY[4,5]),
(3, 1, ARRAY[6]);

INSERT INTO user_message (user_id_1, user_id_2, messages) VALUES
(1, 2, ARRAY['Привет!', 'Как дела?']),
(2, 1, ARRAY['Привет!', 'Хорошо!']);

INSERT INTO user_matches (user_id_1, user_id_2, user_matches) VALUES
(1, 2, ARRAY[1,2,3]),
(2, 1, ARRAY[1,2,3]);

SELECT 
    u.user_id,
    u.user_age,
    u.user_location,
    d.user_description,
    d.user_values,
    d.user_children,
    d.user_desc_children,
    d.user_hobbies,
    d.user_personal_traits,
    d.user_target_life,
    p.user_login,
    p.user_pwd,
    p.user_email,
    f.user_InFavorit_id AS favorite_user,
    f.user_messages AS sent_messages,
    m1.messages AS received_messages,
    mt.user_matches AS matches
FROM user_info_table u
JOIN user_description_table d ON u.user_id = d.user_id
JOIN user_personality_data p ON u.user_id = p.user_id
LEFT JOIN user_favorites_likes f ON u.user_id = f.user_id
LEFT JOIN user_message m1 ON u.user_id = m1.user_id_1
LEFT JOIN user_message m2 ON u.user_id = m2.user_id_2
LEFT JOIN user_matches mt ON u.user_id = mt.user_id_1;



