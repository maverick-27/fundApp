# Steps to run this app :
   
   ## pip install flask
   ## pip install flask_mysqldb
   ## flask run -h localhost -p 3000



# Make sure DB is running in parallel
  
  ## create database fundsapp;
  ## use database fundsapp;
     
      create table fundsapp (
      version varchar(100),
      fund_short_name varchar(100),
      supplier varchar(100),
      fund_type varchar(100),
      created_date datetime,
      updated_date datetime,
      created_by varchar(100),
      updated_by varchar(100),
      active_indicator varchar(50),
      constraint fundsapp primary key(fund_short_name,updated_date)	
   );
