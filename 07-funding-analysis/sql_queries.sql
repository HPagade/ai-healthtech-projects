-- Healthcare Startup Funding Analysis SQL Queries
-- Sample queries for analyzing funding data

-- ============================================================================
-- 1. OVERALL FUNDING STATISTICS
-- ============================================================================

-- Total funding by year
SELECT
    year,
    COUNT(*) as num_deals,
    SUM(funding_amount) / 1000000 as total_funding_millions,
    AVG(funding_amount) / 1000000 as avg_deal_size_millions,
    MIN(funding_amount) / 1000000 as min_deal_millions,
    MAX(funding_amount) / 1000000 as max_deal_millions
FROM funding_data
GROUP BY year
ORDER BY year DESC;

-- Funding by quarter
SELECT
    year,
    quarter,
    COUNT(*) as num_deals,
    SUM(funding_amount) / 1000000 as total_funding_millions
FROM funding_data
GROUP BY year, quarter
ORDER BY year DESC, quarter;

-- ============================================================================
-- 2. CATEGORY ANALYSIS
-- ============================================================================

-- Top funded categories
SELECT
    category,
    COUNT(*) as num_companies,
    SUM(funding_amount) / 1000000 as total_funding_millions,
    AVG(funding_amount) / 1000000 as avg_deal_size_millions
FROM funding_data
GROUP BY category
ORDER BY total_funding_millions DESC;

-- Category trends over time
SELECT
    year,
    category,
    COUNT(*) as num_deals,
    SUM(funding_amount) / 1000000 as total_funding_millions
FROM funding_data
GROUP BY year, category
ORDER BY year DESC, total_funding_millions DESC;

-- ============================================================================
-- 3. FUNDING STAGE ANALYSIS
-- ============================================================================

-- Deals by stage
SELECT
    funding_stage,
    COUNT(*) as num_deals,
    SUM(funding_amount) / 1000000 as total_funding_millions,
    AVG(funding_amount) / 1000000 as avg_deal_size_millions,
    MIN(funding_amount) / 1000000 as min_deal_millions,
    MAX(funding_amount) / 1000000 as max_deal_millions
FROM funding_data
GROUP BY funding_stage
ORDER BY
    CASE funding_stage
        WHEN 'Seed' THEN 1
        WHEN 'Series A' THEN 2
        WHEN 'Series B' THEN 3
        WHEN 'Series C' THEN 4
        WHEN 'Series D+' THEN 5
    END;

-- Stage progression by year
SELECT
    year,
    funding_stage,
    COUNT(*) as num_deals,
    SUM(funding_amount) / 1000000 as total_millions
FROM funding_data
GROUP BY year, funding_stage
ORDER BY year DESC;

-- ============================================================================
-- 4. GEOGRAPHIC ANALYSIS
-- ============================================================================

-- Top locations by deal count
SELECT
    location,
    COUNT(*) as num_deals,
    SUM(funding_amount) / 1000000 as total_funding_millions,
    AVG(funding_amount) / 1000000 as avg_deal_size_millions
FROM funding_data
GROUP BY location
ORDER BY total_funding_millions DESC
LIMIT 10;

-- ============================================================================
-- 5. INVESTOR ANALYSIS
-- ============================================================================

-- Most active investors (requires unnesting investors column)
-- Note: This query structure depends on your SQL database type
-- For PostgreSQL with array support:
/*
SELECT
    TRIM(investor) as investor_name,
    COUNT(*) as num_investments,
    SUM(funding_amount) / 1000000 as total_invested_millions
FROM funding_data,
     LATERAL unnest(string_to_array(investors, ', ')) as investor
GROUP BY investor_name
ORDER BY num_investments DESC
LIMIT 20;
*/

-- YC-backed vs non-YC companies
SELECT
    has_yc_backing,
    COUNT(*) as num_companies,
    SUM(funding_amount) / 1000000 as total_funding_millions,
    AVG(funding_amount) / 1000000 as avg_deal_size_millions,
    AVG(total_raised) / 1000000 as avg_total_raised_millions
FROM funding_data
GROUP BY has_yc_backing;

-- ============================================================================
-- 6. ADVANCED ANALYTICS
-- ============================================================================

-- Companies with largest single rounds
SELECT
    company_name,
    category,
    funding_stage,
    funding_amount / 1000000 as funding_millions,
    funding_date,
    location,
    investors
FROM funding_data
ORDER BY funding_amount DESC
LIMIT 20;

-- Mega rounds (>$50M)
SELECT
    company_name,
    category,
    funding_stage,
    funding_amount / 1000000 as funding_millions,
    funding_date,
    location
FROM funding_data
WHERE funding_amount > 50000000
ORDER BY funding_amount DESC;

-- Most capital efficient companies (high total raised with few investors)
SELECT
    company_name,
    category,
    total_raised / 1000000 as total_raised_millions,
    n_investors,
    (total_raised / n_investors) / 1000000 as avg_per_investor_millions,
    location
FROM funding_data
WHERE n_investors > 0
ORDER BY avg_per_investor_millions DESC
LIMIT 20;

-- Year-over-year growth
SELECT
    year,
    COUNT(*) as num_deals,
    SUM(funding_amount) / 1000000 as total_funding_millions,
    LAG(SUM(funding_amount)) OVER (ORDER BY year) / 1000000 as prev_year_millions,
    ROUND(
        ((SUM(funding_amount) - LAG(SUM(funding_amount)) OVER (ORDER BY year))
         / LAG(SUM(funding_amount)) OVER (ORDER BY year)) * 100,
        2
    ) as yoy_growth_pct
FROM funding_data
GROUP BY year
ORDER BY year;

-- ============================================================================
-- 7. COHORT ANALYSIS
-- ============================================================================

-- Seed stage companies by category
SELECT
    category,
    COUNT(*) as num_seed_deals,
    AVG(funding_amount) / 1000000 as avg_seed_size_millions
FROM funding_data
WHERE funding_stage = 'Seed'
GROUP BY category
ORDER BY num_seed_deals DESC;

-- Companies that raised in last 12 months
SELECT
    company_name,
    category,
    funding_stage,
    funding_amount / 1000000 as funding_millions,
    funding_date,
    location
FROM funding_data
WHERE funding_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
ORDER BY funding_date DESC;

-- ============================================================================
-- 8. MARKET INSIGHTS
-- ============================================================================

-- Average time between rounds (requires multiple funding records per company)
-- This is a simplified version
SELECT
    category,
    funding_stage,
    COUNT(*) as num_companies,
    AVG(funding_amount) / 1000000 as avg_amount_millions
FROM funding_data
GROUP BY category, funding_stage
ORDER BY category, funding_stage;

-- Market concentration (Herfindahl-Hirschman Index by category)
WITH category_shares AS (
    SELECT
        category,
        SUM(funding_amount) as category_funding,
        (SELECT SUM(funding_amount) FROM funding_data) as total_funding
    FROM funding_data
    GROUP BY category
)
SELECT
    category,
    category_funding / 1000000 as funding_millions,
    ROUND((category_funding / total_funding) * 100, 2) as market_share_pct
FROM category_shares
ORDER BY market_share_pct DESC;

-- ============================================================================
-- 9. EXPORT QUERIES
-- ============================================================================

-- Create summary table for Tableau
CREATE TABLE IF NOT EXISTS funding_summary AS
SELECT
    year,
    quarter,
    category,
    funding_stage,
    location,
    COUNT(*) as deal_count,
    SUM(funding_amount) / 1000000 as total_funding_millions,
    AVG(funding_amount) / 1000000 as avg_deal_size_millions
FROM funding_data
GROUP BY year, quarter, category, funding_stage, location;

-- Export full dataset with calculated fields
SELECT
    *,
    funding_amount / 1000000 as funding_millions,
    total_raised / 1000000 as total_raised_millions,
    YEAR(funding_date) as funding_year,
    QUARTER(funding_date) as funding_quarter
FROM funding_data;
