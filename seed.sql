CREATE TYPE reg_type AS ENUM ('checkin', 'checkout');

CREATE TABLE people (
    id      integer primary key generated always as identity,
    name    text not null,
    cardno  integer
);

CREATE TABLE checkins (
    id      integer primary key generated always as identity,
    person_id integer,
    type    reg_type not null,
    time    timestamp not null default date_trunc('second', now()),

    CONSTRAINT fk_person
        FOREIGN KEY (person_id)
            REFERENCES people(id)
);
