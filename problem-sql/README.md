###  Question 1
Write an Amazon Athena (or Presto) SQL query that creates a table from the reservations table,
that shows only the most recent state of each room that has not been reserved yet. Store the new
table in PARQUET data format and partition by checkin_date .

```
CREATE EXTERNAL TABLE room_recent_status as
(
    with latest_reservation_status as (
        SELECT ROW_NUMBER () OVER ( 
            PARTITION BY room_number
            ORDER BY checkout_date 
        ) row_number,room_number,reservation_status,checkin_date,checkout_date
        FROM reservations
        where reservation_status = 'OPEN' -- as we need most recent status of room that has not been reserved
    ) select room_number,reservation_status,checkin_date,checkout_date
    from latest_reservation_status 
    where row_number = 1
)
PARTITIONED BY (checkin_date STRING)
STORED AS PARQUET
LOCATION 's3://example/loc'
tblproperties ("parquet.compression"="SNAPPY");
```

### Question 2 
Assuming that analysts and data consultants often filter on the reservation_status column. To reduce the amount of data scanned
by Amazon Athena and at the same time improve query speed, what other techniques can you put in place to fulfill this

```
If above statement is for table reservations 

1. Use Columnar storage to store data, it will help in fast filtering and fetching data.
2. While querying analysts and data consultants should use proper filters, should have partion coloumn in query i.e if partition is on checkin_date it must be there in the query.
3. Only include the coloumns that you need in SQL Query.
4. Use limit along with order by if only some records need to be fetched.
5. Optimize files size (Ideally have files atleast of 1GB if not 128mb, 256mb), Use compresseion like snappy to store more data in single file.
6. Bucketing over reservation_status coloumn.

```