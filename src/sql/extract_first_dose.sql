WITH drug_intake_sequence AS (
  SELECT subject_id,
       drug,
       starttime,
       ROW_NUMBER() OVER(PARTITION BY subject_id, drug ORDER BY starttime ASC) AS drug_intake
  FROM physionet-data.mimiciv_3_1_hosp.prescriptions
)
SELECT subject_id,
       drug,
       starttime,
       drug_intake
FROM drug_intake_sequence
WHERE drug_intake = 1
ORDER BY subject_id, drug
LIMIT 50