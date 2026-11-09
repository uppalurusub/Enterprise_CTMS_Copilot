use enterprise_ctms;
CREATE TABLE recruitment(

    recruitment_id VARCHAR(20) PRIMARY KEY,

    study_id VARCHAR(20),

    site_id VARCHAR(20),

    screening_count INT,

    enrolled_count INT,

    randomized_count INT,

    completed_count INT,

    dropout_count INT,

    recruitment_status VARCHAR(30),

    FOREIGN KEY(study_id)

    REFERENCES studies(study_id),

    FOREIGN KEY(site_id)

    REFERENCES sites(site_id)
);