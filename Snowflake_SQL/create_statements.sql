CREATE DATABASE STOCK_ANALYSIS_APP;

CREATE OR REPLACE TABLE users (
  email VARCHAR(255),
  password VARCHAR(255),
  -- password variant,
  signup_date DATETIME,
  service_plan VARCHAR(50),
  admin_flag BOOLEAN default false
);

-- admin
insert into users 
values ('admin', 'admin', '2023-04-19 17:33:41.000', 'Free', True);

CREATE OR REPLACE TABLE logging (
  email VARCHAR(255),
  run_date DATETIME,
  stock VARCHAR(50),
  service_plan VARCHAR(50),
  result VARCHAR(255)
);

-- truncate table user;
-- truncate table logging;