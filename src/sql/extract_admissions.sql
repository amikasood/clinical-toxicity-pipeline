WITH admissions AS (
  SELECT subject_id, 
         hadm_id,
         admittime,
         LAG(admittime) OVER(PARTITION BY subject_id ORDER BY admittime ASC) AS previous_admittime
  FROM `physionet-data.mimiciv_3_1_hosp.admissions`
)
SELECT subject_id, 
       hadm_id, 
       admittime,
       previous_admittime,
       DATETIME_DIFF(admittime, previous_admittime, DAY) AS days_lag
FROM admissions
ORDER BY subject_id, admittime ASC
LIMIT 50