import psycopg2
import sys
from config import load_config
from psycopg2.extras import execute_values


#Returns True if the provided table (default employees) exists, returns False otherwise
def table_exists(table="employees"):
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name='{table}')") #Determines if the employees table exists
                return cur.fetchone()[0]
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

#Creates the employees table for the sql database
#Shoulde only be used to make employees, table variable for testing purposes
def create_tables(table="employees"):
    command = ( #Command to create table. More standardized names.
        #SERIAL PRIMARY KEY might cause new emplyees to be skipped if they use default SERIAL number. 
        #over_18, daily_rate, monthly_income, and employee_count removed. years_with_curr_manager became years_with_current_manager
        #assume people who do not have all fields filled out are new employees
        #NOTE: Currently inserting Null into fields with DEFAULT
        f"""
        CREATE TABLE {table}(
            employee_number SERIAL PRIMARY KEY,
            age INTEGER NOT NULL CHECK (age > 17),
            attrition BOOLEAN DEFAULT FALSE,
            business_travel VARCHAR(20) NOT NULL,
            department VARCHAR(30) NOT NULL,
            distance_from_home INTEGER CHECK (distance_from_home > -1),
            education INTEGER NOT NULL CHECK (education > 0 AND education < 6),
            education_field VARCHAR(30) NOT NULL,
            environment_satisfaction INTEGER CHECK (environment_satisfaction > 0 AND environment_satisfaction < 6),
            gender VARCHAR(20),
            hourly_rate INTEGER NOT NULL CHECK (hourly_rate > 0),
            job_involvement INTEGER CHECK (job_involvement > 0 AND job_involvement < 6),
            job_level INTEGER NOT NULL CHECK (job_level > 0 AND job_level < 6),
            job_role VARCHAR(30) NOT NULL,
            marital_status VARCHAR(10),
            monthly_rate INTEGER NOT NULL CHECK (monthly_rate > 0),
            num_companies_worked INTEGER CHECK (num_companies_worked > -1),
            overtime BOOLEAN DEFAULT FALSE,
            percent_salary_hike INTEGER DEFAULT 0,
            performance_rating INTEGER CHECK (performance_rating > 0 AND performance_rating < 6),
            relationship_satisfaction INTEGER CHECK (relationship_satisfaction > 0 AND relationship_satisfaction < 6),
            standard_hours INTEGER DEFAULT 80 CHECK (standard_hours > 0),
            stock_option_level INTEGER CHECK (stock_option_level > -1),
            total_working_years INTEGER CHECK (total_working_years > -1),
            training_times_last_year INTEGER CHECK (training_times_last_year > -1),
            work_life_balance INTEGER CHECK (work_life_balance > 0 AND work_life_balance < 6),
            years_at_company INTEGER DEFAULT 0 CHECK (years_at_company > -1),
            years_in_current_role INTEGER DEFAULT 0 CHECK (years_in_current_role > -1),
            years_since_last_promotion INTEGER DEFAULT 0 CHECK (years_since_last_promotion > -1),
            years_with_current_manager INTEGER DEFAULT 0 CHECK (years_with_current_manager > -1)
        )
        """)
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                if(not table_exists(table)): #If table doesn't exist
                    cur.execute(command)
                    print(f"{table} table created")
                else: #Shouldn't happen from main function
                    print(f"{table} table already exists")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

        

#Fills database with values given a list of inputs that contain ordered parameters. Returns updates and inserts for logging purposes.
def fill_database(input_list, table="employees"): #table for testing purposes
    sql = f"INSERT INTO {table}(employee_number, age, attrition, business_travel, department, distance_from_home," \
    "education, education_field, environment_satisfaction, gender, hourly_rate, job_involvement, job_level," \
    "job_role, marital_status, monthly_rate, num_companies_worked, overtime, percent_salary_hike, performance_rating," \
    "relationship_satisfaction, standard_hours, stock_option_level, total_working_years, training_times_last_year," \
    "work_life_balance, years_at_company, years_in_current_role, years_since_last_promotion, years_with_current_manager) " \
    "VALUES %s"\
    "ON CONFLICT (employee_number) DO UPDATE SET " \
    "(age, attrition, business_travel, department, distance_from_home, education, education_field, environment_satisfaction,"\
    "gender, hourly_rate, job_involvement, job_level, job_role, marital_status, monthly_rate, num_companies_worked, overtime,"\
    "percent_salary_hike, performance_rating, relationship_satisfaction, standard_hours, stock_option_level, total_working_years,"\
    "training_times_last_year, work_life_balance, years_at_company, years_in_current_role, years_since_last_promotion, years_with_current_manager) "\
    "= (EXCLUDED.age, EXCLUDED.attrition, EXCLUDED.business_travel, EXCLUDED.department, EXCLUDED.distance_from_home,"\
    "EXCLUDED.education, EXCLUDED.education_field, EXCLUDED.environment_satisfaction, EXCLUDED.gender, EXCLUDED.hourly_rate,"\
    "EXCLUDED.job_involvement, EXCLUDED.job_level, EXCLUDED.job_role, EXCLUDED.marital_status, EXCLUDED.monthly_rate,"\
    "EXCLUDED.num_companies_worked, EXCLUDED.overtime, EXCLUDED.percent_salary_hike, EXCLUDED.performance_rating,"\
    "EXCLUDED.relationship_satisfaction, EXCLUDED.standard_hours, EXCLUDED.stock_option_level, EXCLUDED.total_working_years,"\
    "EXCLUDED.training_times_last_year, EXCLUDED.work_life_balance, EXCLUDED.years_at_company, EXCLUDED.years_in_current_role,"\
    "EXCLUDED.years_since_last_promotion, EXCLUDED.years_with_current_manager)"\
    "RETURNING (xmax=0) AS inserted;"
    config = load_config()
    try:
        if table_exists(table):
            with  psycopg2.connect(**config) as conn:
                with  conn.cursor() as cur:
                    #cur.executemany(sql, input_list)
                    execute_values(cur, sql, input_list, page_size=len(input_list))
                    results = cur.fetchall()

                conn.commit()
                inserted = sum(inserted for (inserted,) in results)
                updated = len(results) - inserted
                print(f"Employee table updated {updated} rows and inserted {inserted} rows.")
                return (inserted, updated)
        else:
            print(f"Error: Tried filling table {table}, which doesn't exist")
            return (None, None)
    except (Exception, psycopg2.DatabaseError) as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f"Error: The following error occured trying to insert into the database: {error} on line {exc_tb.tb_lineno}")

#Drops the employee table. Mostly used for resetting the employee table.
def drop_table(table="employees"):
    try:
        config = load_config()
        sql = f"DROP TABLE {table}"
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                if(table_exists(table)): #If table exists
                    cur.execute(sql)
                    print(f"Table {table} dropped")
                else:
                    print(f"{table} table does not exist")
    except (psycopg2.DatabaseError, Exception) as e:
        print(f"Failed to drop table Employees: {e}")

#Clears/Truncates the employee table of data. Mostly used for resetting the employee table data.
def clear_table():
    try:
        config = load_config()
        sql = "TRUNCATE TABLE employees" #removes all data in employees
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                if(table_exists()): #If table exists
                    cur.execute(sql)
                    print("Table Employees truncated")
                else:
                    print("Employees table does not exist")
    except (psycopg2.DatabaseError, Exception) as e:
        print(f"Failed to clear table Employees: {e}")

#Reads the table and prints it line by line
def read_table():
    config = load_config()
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                cur.execute("SELECT * FROM employees")
                rows = cur.fetchall()
                for row in rows:
                    print(row)

    except (Exception, psycopg2.DatabaseError) as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f"Error: The following error occured trying to read the database: {error} on line {exc_tb.tb_lineno}")

#Counts the number of rows in the provided table. Mostly for testing purposes
def count_rows(table="employees"):
    config = load_config()
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                rows = cur.fetchone()[0]
                return rows

    except (Exception, psycopg2.DatabaseError) as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f"Error: The following error occured trying to count rows: {error} on line {exc_tb.tb_lineno}")