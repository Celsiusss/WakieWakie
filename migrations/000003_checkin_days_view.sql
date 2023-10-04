CREATE VIEW checkin_days AS
    SELECT person_id, DATE(time) AS d, EXTRACT(ISODOW FROM date(time)) dow, SUM(duration) duration
    FROM checkins
    GROUP BY person_id, d, dow;
