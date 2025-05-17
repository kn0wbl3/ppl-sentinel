-- tables
CREATE TABLE IF NOT EXISTS aides (
    pa_ppl_id VARCHAR(20) PRIMARY KEY,
    pa_name VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS shifts (
    shift_id VARCHAR(20) PRIMARY KEY,
    pa_ppl_id VARCHAR(20),
    date_time_in TIMESTAMP,
    date_time_out TIMESTAMP,
    -- payroll_period VARCHAR(40),
    shift_status VARCHAR(50),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pa_ppl_id FOREIGN KEY (pa_ppl_id)
        REFERENCES aides(pa_ppl_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS shift_history (
    shift_id VARCHAR(20),
    pa_ppl_id VARCHAR(20),
    date_time_in TIMESTAMP,
    date_time_out TIMESTAMP,
    -- payroll_period VARCHAR(40),
    shift_status VARCHAR(50),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    -- CONSTRAINT fk_shift_id FOREIGN KEY (shift_id)
    --     REFERENCES shifts(shift_id)
    --     ON DELETE CASCADE
);

-- function and trigger for shift_id
CREATE OR REPLACE FUNCTION generate_shift_id()
RETURNS TRIGGER AS $$
DECLARE
    ppl_suffix TEXT;
    in_suffix TEXT;
    out_suffix TEXT;
BEGIN
    ppl_suffix := RIGHT(NEW.pa_ppl_id, 4);
    in_suffix := TO_CHAR(NEW.date_time_in, 'YYYYMMDD_HH24MI');

    NEW.shift_id := ppl_suffix || in_suffix;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_shift_id
BEFORE INSERT ON shifts
FOR EACH ROW
EXECUTE FUNCTION generate_shift_id();

CREATE TRIGGER set_shift_id
BEFORE INSERT ON shift_history
FOR EACH ROW
EXECUTE FUNCTION generate_shift_id();

-- function and trigger for current timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER set_updated_at
BEFORE UPDATE ON shifts
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
