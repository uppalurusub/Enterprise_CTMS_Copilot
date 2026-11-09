use enterprise_ctms;
CREATE TABLE corrective_actions(

    capa_id VARCHAR(20) PRIMARY KEY,

    visit_id VARCHAR(20),

    action_description TEXT,

    owner VARCHAR(100),

    due_date DATE,

    priority VARCHAR(20),

    status VARCHAR(30),

    completion_date DATE,

    FOREIGN KEY(visit_id)

    REFERENCES monitoring_visits(visit_id)
);