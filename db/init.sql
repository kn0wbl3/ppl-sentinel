CREATE TABLE IF NOT EXISTS aides (
    pa_ppl_id VARCHAR(20) PRIMARY KEY,
    pa_name VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS shifts (
    shift_id SERIAL PRIMARY KEY,
    pa_ppl_id VARCHAR(20),
    date_time_in TIMESTAMP,
    date_time_out TIMESTAMP,
    payroll_period VARCHAR(40),
    shift_status VARCHAR(50),
    CONSTRAINT fk_pa_ppl_id FOREIGN KEY (pa_ppl_id)
        REFERENCES aides(pa_ppl_id)
        ON DELETE CASCADE
);
