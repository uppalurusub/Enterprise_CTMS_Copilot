use enterprise_ctms;

CREATE TABLE studies (

    study_id VARCHAR(20) PRIMARY KEY,

    protocol_id VARCHAR(20) NOT NULL,

    study_name VARCHAR(200),

    phase VARCHAR(20),

    therapeutic_area VARCHAR(100),

    sponsor VARCHAR(150),

    indication VARCHAR(150),

    start_date DATE,

    end_date DATE,

    target_enrollment INT,

    status VARCHAR(30),

    country VARCHAR(100)
);