-- 1. Isolate the exact first exposure to the target drugs
-- Rank exposures
WITH target_prescription AS (
  SELECT p.subject_id,
         p.hadm_id,
         p.drug,
         p.starttime,
         hep.chembl_id,
         ROW_NUMBER() OVER(PARTITION BY p.subject_id, p.drug ORDER BY p.starttime ASC) AS drug_intake
  FROM `physionet-data.mimiciv_3_1_hosp.prescriptions` AS p
  JOIN `techbio-mimic-sandbox.clinical_pipeline.hepatotoxic_drugs` AS hep
    ON LOWER(p.drug) = hep.drug_name
),

-- Extract first exposures
first_exposure AS (
  SELECT * FROM target_prescription WHERE drug_intake = 1
),

-- 2. Find the Baseline, the most recent lab drawn before the drug
baseline_labs_raw AS (
  SELECT fe.subject_id,
         fe.hadm_id,
         fe.drug,
         fe.chembl_id,
         fe.starttime,
         le.itemid,
         le.valuenum AS baseline_val,
         -- Order descending to rank the most recent past lab as #1
         ROW_NUMBER() OVER(PARTITION BY fe.subject_id, fe.hadm_id, le.itemid ORDER BY le.charttime DESC) AS recent_lab_rank
  FROM first_exposure AS fe
  JOIN `physionet-data.mimiciv_3_1_hosp.labevents` AS le
    ON fe.subject_id = le.subject_id AND fe.hadm_id = le.hadm_id
  WHERE le.charttime <= fe.starttime
    AND le.itemid IN (50861, 50878)
),

baseline_labs AS (
  SELECT * FROM baseline_labs_raw WHERE recent_lab_rank = 1
),

-- 3. Find the Peak, the highest lab drawn within 72 hours after the drug)
peak_labs AS (
  SELECT fe.subject_id,
         fe.hadm_id,
         fe.drug,
         fe.chembl_id,
         fe.starttime,
         le.itemid,
         MAX(le.valuenum) AS peak_val
  FROM first_exposure AS fe
  JOIN `physionet-data.mimiciv_3_1_hosp.labevents` AS le
    ON fe.subject_id = le.subject_id AND fe.hadm_id = le.hadm_id
  WHERE le.charttime > fe.starttime
    AND le.charttime <= DATETIME_ADD(fe.starttime, INTERVAL 72 HOUR)
    AND le.itemid IN (50861, 50878)
  GROUP BY fe.subject_id, fe.hadm_id, fe.drug, fe.chembl_id, fe.starttime, le.itemid
)

-- 4. Calculate the ratio and generate the Toxicity Label
SELECT 
  p.subject_id,
  p.hadm_id,
  p.chembl_id,
  p.drug,
  p.itemid,
  p.starttime AS time_of_exposure,
  b.baseline_val,
  p.peak_val,
  ROUND(p.peak_val / NULLIF(b.baseline_val, 0), 2) AS fold_change,
  CASE 
    WHEN (p.peak_val / NULLIF(b.baseline_val, 0)) >= 3.0 THEN 1 
    ELSE 0 
  END AS Toxicity
FROM peak_labs AS p
JOIN baseline_labs AS b
  ON p.subject_id = b.subject_id 
  AND p.hadm_id = b.hadm_id 
  AND p.drug = b.drug
  AND p.itemid = b.itemid
ORDER BY p.subject_id, p.itemid;
