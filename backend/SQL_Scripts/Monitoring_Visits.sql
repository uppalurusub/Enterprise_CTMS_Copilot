use enterprise_ctms;
CREATE TABLE monitoring_visits(

    visit_id VARCHAR(20) PRIMARY KEY,

    study_id VARCHAR(20),

    site_id VARCHAR(20),

    visit_type VARCHAR(50),

    visit_date DATE,

    cra_name VARCHAR(100),

    findings TEXT,

    deviation_count INT,

    sdv_completed DECIMAL(5,2),

    status VARCHAR(30),

    FOREIGN KEY(study_id)

    REFERENCES studies(study_id),

    FOREIGN KEY(site_id)

    REFERENCES sites(site_id)
);