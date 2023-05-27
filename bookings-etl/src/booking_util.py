from pyspark.sql import functions as F

def write_to_parquet(df,loc):
    df.write\
    .mode('overwrite')\
    .parquet(loc)
    
def read_csv(spark_session, loc,header='false'):
    return spark_session.read.format('csv')\
    .option('header',header)\
    .load(loc)

def calculate_arrival_date(df):
    return df.withColumn('arrival_date',
        F.to_date(
            F.concat_ws(
                "-",F.col("arrival_date_year"),F.col("arrival_date_month"),F.col("arrival_date_day_of_month")
            ),"yyyy-MMM-dd")
    )
    
def calculate_departure_date(df):
    return  df.withColumn('departure_date',
                            F.expr("date_add(arrival_date, cast(stays_in_weekend_nights as int)+cast(stays_in_week_nights as int))")
                         )

def is_with_family_breakfast(df):
    return df\
        .withColumn('no_of_children', F.col('children')+F.col('babies'))\
        .withColumn('with_family_breakfast', F.when(F.expr('no_of_children > 0'), F.lit('YES')).otherwise(F.lit('NO')))\
        .drop('no_of_children')