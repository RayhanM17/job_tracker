USE job_tracker;
INSERT INTO companies (company_name, industry, website, city, state, notes) VALUES
 ('TechCorp','Software','https://techcorp.example','Miami','FL','Great remote policy'),
 ('DataCo','Analytics','https://dataco.example','Austin','TX','Referred by a friend'),
 ('CloudNine','Cloud','https://cloudnine.example','Seattle','WA',NULL);
INSERT INTO jobs (company_id, job_title, job_type, salary_min, salary_max, job_url, date_posted, requirements) VALUES
 (1,'Software Developer','Full-time',80000,110000,'https://techcorp.example/jobs/1','2026-11-01','["Python","SQL","Flask"]'),
 (2,'Data Analyst','Full-time',70000,95000,'https://dataco.example/jobs/2','2026-11-05','["Python","SQL","Tableau"]'),
 (3,'Cloud Intern','Internship',25000,30000,NULL,'2026-11-10','["Linux","AWS","Python"]');
INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent, interview_data) VALUES
 (1,'2026-11-03','Interview','v2',TRUE,'{"round":1,"interviewer":"Sam","date":"2026-11-20"}'),
 (2,'2026-11-06','Applied','v2',FALSE,NULL),
 (3,'2026-11-11','Rejected','v1',TRUE,NULL);
INSERT INTO contacts (company_id, contact_name, title, email, phone, linkedin_url, notes) VALUES
 (1,'Sam Rivera','Recruiter','sam@techcorp.example','555-0101','https://linkedin.com/in/samrivera','Met at career fair'),
 (2,'Priya Shah','Hiring Manager','priya@dataco.example','555-0102',NULL,NULL);
