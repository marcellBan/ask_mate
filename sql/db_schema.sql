DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id serial primary key,
    registration_date timestamp without time zone,
    user_name text unique,
    password text
);


DROP TABLE IF EXISTS question;

CREATE TABLE question (
    id serial primary key,
    user_id integer not null references users(id),
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text,
    has_accepted_answer boolean not null default FALSE
);


DROP TABLE IF EXISTS answer;

CREATE TABLE answer (
    id serial primary key,
    question_id integer not null references question(id),
    user_id integer not null references users(id),
    submission_time timestamp without time zone,
    vote_number integer,
    message text,
    image text,
    accepted_answer boolean not null default FALSE
);


DROP TABLE IF EXISTS comment;

CREATE TABLE comment (
    id serial primary key,
    question_id integer references question(id),
    answer_id integer references answer(id),
    user_id integer not null references users(id),
    message text,
    submission_time timestamp without time zone,
    edit_count integer
);
