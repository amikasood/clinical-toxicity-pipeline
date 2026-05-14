-- Filter drugs using the input table
WITH target_prescription AS (
  SELECT p.subject_id,
       p.hadm_id,
       p.drug,
       p.starttime,
       hep.chembl_id,
       ROW_NUMBER() OVER(PARTITION BY subject_id, drug ORDER BY starttime ASC) AS drug_intake
  FROM `physionet-data.mimiciv_3_1_hosp.prescriptions` AS p
  JOIN techbio-mimic-sandbox.clinical_pipeline.hepatotoxic_drugs AS hep
  ON LOWER(p.drug) = hep.drug_name
),

-- 50861: ALT, 50878: AST
first_dose AS (
   SELECT tp.subject_id,
       tp.hadm_id,
       tp.drug,
       tp.chembl_id,
       tp.starttime,
       tp.drug_intake,
       le.itemid,
       le.valuenum
   FROM target_prescription AS tp
   JOIN `physionet-data.mimiciv_3_1_hosp.labevents` AS le
   ON tp.subject_id = le.subject_id AND tp.hadm_id = le.hadm_id
   WHERE le.charttime > tp.starttime AND le.charttime <= DATETIME_ADD(tp.starttime, INTERVAL 72 HOUR) AND le.itemid IN (50861, 50878) AND tp.drug_intake = 1
)

SELECT subject_id,
       hadm_id,
       drug,
       chembl_id,
       itemid,
       starttime AS time_of_exposure,
       MAX(valuenum) AS maximum_enzyme_expression,       
       CASE 
         WHEN itemid = 50861 AND MAX(valuenum) > 150 THEN 1
         WHEN itemid = 50878 AND MAX(valuenum) > 150 THEN 1
         ELSE 0
       END AS Toxicity
FROM first_dose
GROUP BY subject_id, hadm_id, drug, chembl_id, itemid, starttime
ORDER BY subject_id, drug
