-- 1. What is the distribution of medical conditions in the dataset?
SELECT 
    medical_condition,
    COUNT(*) AS patient_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM healthcare_dataset), 2) AS percentage
FROM healthcare_dataset
GROUP BY medical_condition
ORDER BY patient_count DESC;

-- 2.Is there a relationship between age and length of hospital stay?
SELECT 
    CASE 
        WHEN age BETWEEN 0 AND 30 THEN '0-30'
        WHEN age BETWEEN 31 AND 50 THEN '31-50'
        WHEN age BETWEEN 51 AND 70 THEN '51-70'
        ELSE '71+'
    END AS age_group,
    COUNT(*) AS patient_count,
    ROUND(AVG(length_of_stay), 2) AS avg_stay,
    MIN(length_of_stay) AS min_stay,
    MAX(length_of_stay) AS max_stay
FROM healthcare_dataset
GROUP BY age_group
ORDER BY age_group;

-- 3. What is the average billing amount by medical condition?
SELECT 
    medical_condition,
    COUNT(*) AS patient_count,
    ROUND(AVG(billing_amount), 2) AS avg_billing,
    ROUND(MIN(billing_amount), 2) AS min_billing,
    ROUND(MAX(billing_amount), 2) AS max_billing
FROM healthcare_dataset
GROUP BY medical_condition
ORDER BY avg_billing DESC;

-- 4.Is there a difference in length of stay by admission type (Emergency, Elective, Urgent)?
SELECT 
    admission_type,
    COUNT(*) AS patient_count,
    ROUND(AVG(length_of_stay), 2) AS avg_stay,
    MIN(length_of_stay) AS min_stay,
    MAX(length_of_stay) AS max_stay
FROM healthcare_dataset
GROUP BY admission_type
ORDER BY avg_stay DESC;

-- 5.What are the most common medications for each medical condition?
WITH RankedMeds AS (
    SELECT 
        medical_condition,
        medication,
        COUNT(*) AS usage_count,
        ROW_NUMBER() OVER (PARTITION BY medical_condition ORDER BY COUNT(*) DESC) AS rank_num
    FROM healthcare_dataset
    GROUP BY medical_condition, medication
)
SELECT 
    medical_condition,
    medication,
    usage_count
FROM RankedMeds
WHERE rank_num = 1
ORDER BY medical_condition;

-- 6.Is there a relationship between blood type and medical conditions?
SELECT 
    blood_type,
    medical_condition,
    COUNT(*) AS patient_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY blood_type), 2) AS percentage_per_blood_type
FROM healthcare_dataset
GROUP BY blood_type, medical_condition
ORDER BY blood_type, patient_count DESC;

-- 7.What is the distribution of test results (Normal, Abnormal, Inconclusive) by medical condition?
SELECT 
    medical_condition,
    test_results,
    COUNT(*) AS result_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY medical_condition), 2) AS percentage
FROM healthcare_dataset
GROUP BY medical_condition, test_results
ORDER BY medical_condition, result_count DESC;

-- 8.Which hospitals treat the highest number of patients?
SELECT 
    hospital,
    COUNT(*) AS patient_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM healthcare_dataset), 2) AS percentage
FROM healthcare_dataset
GROUP BY hospital
ORDER BY patient_count DESC
LIMIT 10;

-- 9.Is there a difference in billing amounts by insurance provider?
SELECT 
    insurance_provider,
    COUNT(*) AS patient_count,
    ROUND(AVG(billing_amount), 2) AS avg_billing,
    ROUND(MIN(billing_amount), 2) AS min_billing,
    ROUND(MAX(billing_amount), 2) AS max_billing
FROM healthcare_dataset
GROUP BY insurance_provider
ORDER BY avg_billing DESC;

-- 10.What is the average length of stay by medical condition and gender?
SELECT 
    medical_condition,
    gender,
    COUNT(*) AS patient_count,
    ROUND(AVG(length_of_stay), 2) AS avg_stay,
    MIN(length_of_stay) AS min_stay,
    MAX(length_of_stay) AS max_stay
FROM healthcare_dataset
GROUP BY medical_condition, gender
ORDER BY medical_condition, gender;

-- 11.Is there an association between age and medical condition?
SELECT 
    medical_condition,
    COUNT(*) AS patient_count,
    ROUND(AVG(age), 2) AS avg_age,
    MIN(age) AS min_age,
    MAX(age) AS max_age
FROM healthcare_dataset
GROUP BY medical_condition
ORDER BY avg_age DESC;

-- 12.What is the distribution of patients by gender in the dataset?
SELECT 
    gender,
    COUNT(*) AS patient_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM healthcare_dataset), 2) AS percentage
FROM healthcare_dataset
GROUP BY gender;

-- 13.Is there a relationship between admission type and test results?
SELECT 
    admission_type,
    test_results,
    COUNT(*) AS result_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY admission_type), 2) AS percentage
FROM healthcare_dataset
GROUP BY admission_type, test_results
ORDER BY admission_type, result_count DESC;

-- 14.What are the most common months for hospital admission?
SELECT 
    MONTH(date_of_admission) AS admission_month,
    COUNT(*) AS admission_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM healthcare_dataset), 2) AS percentage
FROM healthcare_dataset
GROUP BY MONTH(date_of_admission)
ORDER BY admission_count DESC;

-- 15.Is there a difference in billing amounts by length of stay?
SELECT 
    CASE 
        WHEN length_of_stay <= 7 THEN '1-7 days'
        WHEN length_of_stay BETWEEN 8 AND 14 THEN '8-14 days'
        WHEN length_of_stay BETWEEN 15 AND 21 THEN '15-21 days'
        ELSE '22+ days'
    END AS stay_group,
    COUNT(*) AS patient_count,
    ROUND(AVG(billing_amount), 2) AS avg_billing,
    ROUND(MIN(billing_amount), 2) AS min_billing,
    ROUND(MAX(billing_amount), 2) AS max_billing
FROM healthcare_dataset
GROUP BY stay_group
ORDER BY stay_group;