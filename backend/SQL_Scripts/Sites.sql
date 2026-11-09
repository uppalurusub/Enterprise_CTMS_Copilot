
use enterprise_ctms;
CREATE TABLE sites(

    site_id VARCHAR(20) PRIMARY KEY,

    study_id VARCHAR(20),

    site_name VARCHAR(200),

    investigator VARCHAR(150),

    city VARCHAR(100),

    country VARCHAR(100),

    activation_date DATE,

    status VARCHAR(30),

    FOREIGN KEY(study_id)

    REFERENCES studies(study_id)
);