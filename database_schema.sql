USE the_market;

-- ============================================
-- 1. Core company table (Ticker = Primary Key)
-- ============================================
CREATE TABLE companies (
    Ticker VARCHAR(20) PRIMARY KEY,
    Company_name VARCHAR(255) NOT NULL
);

-- ============================================
-- 2. Address details table
-- Ticker is both Primary Key and Foreign Key
-- ============================================
CREATE TABLE company_address (
    Ticker VARCHAR(20) PRIMARY KEY,
    HQ_City VARCHAR(100),
    HQ_State VARCHAR(100),
    HQ_Country VARCHAR(100),
    Full_Address VARCHAR(500),
    CONSTRAINT fk_address_ticker
        FOREIGN KEY (Ticker) REFERENCES companies(Ticker)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ============================================
-- 3. Financial details table
-- ============================================
CREATE TABLE company_financials (
    Ticker VARCHAR(20) PRIMARY KEY,
    Revenue DECIMAL(20,2),       -- in millions, matching your script
    Market_Cap DECIMAL(20,2),    -- in billions, matching your script
    CONSTRAINT fk_financials_ticker
        FOREIGN KEY (Ticker) REFERENCES companies(Ticker)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ============================================
-- 4. Sector / Industry classification table
-- ============================================
CREATE TABLE company_classification (
    Ticker VARCHAR(20) PRIMARY KEY,
    Sector VARCHAR(100),
    Industry VARCHAR(100),
    CONSTRAINT fk_classification_ticker
        FOREIGN KEY (Ticker) REFERENCES companies(Ticker)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ============================================
-- 5. Flat denormalized table (your original one)
-- No foreign keys — standalone reporting table
-- ============================================
CREATE TABLE usa_listed_companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Ticker VARCHAR(20),
    Company_name VARCHAR(255),
    Revenue DECIMAL(20,2),
    Market_Cap DECIMAL(20,2),
    HQ_City VARCHAR(100),
    HQ_State VARCHAR(100),
    HQ_Country VARCHAR(100),
    Sector VARCHAR(100),
    Industry VARCHAR(100)
);
