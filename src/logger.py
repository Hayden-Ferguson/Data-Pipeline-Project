from datetime import datetime

#Start a new logger session given source, number of rows from source, and path to source
#TODO: modify this once we have YAML configuration to not need source and path
def log_start(source, rows, path, file="logger.txt"):
    with open(file, "a") as logger:
        logger.write(f"\n-----{datetime.now()}-----\n")
        logger.write(f"INFO ingest.start source={source} rows={rows} path={path}\n")

#Log the results of data validation given source and the results
def log_validation(source, results, file="logger.txt"):
    with open(file, "a") as logger:
        logger.write(f"INFO ingest.validate source={source} valid={len(results[0])} invalid={len(results[1])}\n")

#Log the results of inserting data given source, number of inserted rows, number of updated rows, and the start time
def log_load(source, inserted, updated, start, file="logger.txt"):
    timer = (datetime.now() - start).total_seconds()
    with open(file, "a") as logger:
        logger.write(f"INFO ingest.load source={source} inserted={inserted} updated={updated} duration={timer}s\n")

#Finishes log given source and status, which is presumed to be success
def log_end(source, status="success", file="logger.txt"):
    with open(file, "a") as logger:
        logger.write(f"INFO ingest.end source={source} status={status}\n")

#Logs rejected data with reasons. This goes to a rejection_log.txt instead of logger.txt
#TODO: if possible change to a reject SQL table
def log_rejects(rejections, file="rejection_log.txt"):
    if len(rejections)>0: #If there are rejections
        with open(file, "a") as logger:
            logger.write(f"\n-----{datetime.now()}-----\n")
            for reject in rejections:
                logger.write(f"{reject[0]}\nreason: {reject[1]}\n")
