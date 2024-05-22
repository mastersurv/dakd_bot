import asyncio
import asyncpg
from tabulate import tabulate
from datetime import datetime, timedelta


class DataBase:
    def __init__(self, db_name, user, password, host='localhost', port=4432):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    async def connect(self):
        self.conn = await asyncpg.connect(
            database=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    async def execute_query(self, query, *args):
        if self.conn is None:
            await self.connect()
        result = await self.conn.fetch(query, *args)
        return result

    async def return_tasks_with_status(self, status):
        return await self.execute_query(
            """
        WITH DurationCTE AS (
            SELECT 
                a."ID",
                a."Name" AS app_name,
                er."Status",
                er."StartTime",
                EXTRACT(EPOCH FROM (NOW() - er."StartTime")) AS duration_seconds
            FROM "ReloadTasks" rt,
                "ReloadTaskOperationals" rto,
                "Apps" a,
                "ExecutionResults" er,
                ( SELECT er2."TaskID",
                        max(er2."CreatedDate") AS crd
                   FROM "ExecutionResults" er2
                  GROUP BY er2."TaskID") er1
            WHERE ((rt."Operational_ID" = rto."ID") AND (rt."App_ID" = a."ID") AND (rt."ID" = er."TaskID") 
            AND (er."TaskID" = er1."TaskID") AND (er."CreatedDate" = er1.crd) 
            AND (rt."Enabled" = true) AND (er."Status"=$1))
        )
        SELECT * FROM DurationCTE
        WHERE duration_seconds < 86400;
            """,  (status)
        )

    async def close(self):
        await self.conn.close()

    async def get_tasks_table(self, status) -> str:
        tasks = await self.return_tasks_with_status(status)
        status_name = {
            2: "Started", 6: "Aborted", 7: "Success", 8: "Failed"
        }

        # Prepare the data for tabulate
        table_data = []
        for record in tasks:
            formatted_time = record['StartTime'].strftime('%Y-%m-%d %H:%M:%S')
            time_obj = datetime.strptime(formatted_time, '%Y-%m-%d %H:%M:%S')
            new_time_obj = time_obj + timedelta(hours=3)  # Добавление 3 часов
            formatted_time = new_time_obj.strftime('%Y-%m-%d %H:%M:%S')
            duration_seconds = record['duration_seconds'] - 10800  # 10800с = 3часа (разница из-за UTC)
            hours, remainder = divmod(duration_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_duration = f"{str(int(hours)).zfill(2)}:{str(int(minutes)).zfill(2)}:{str(int(seconds)).zfill(2)}"
            row = [record['ID'], record['app_name'], formatted_duration, status_name[status], formatted_time]
            table_data.append(row)

        # Define the headers for the table
        headers = ["ID", "App Name", "Duration", "Status", "Start Time"]

        # Generate the table string
        result = tabulate(table_data, headers=headers, tablefmt="grid")

        return result

    async def get_tasks(self, status) -> str:
        tasks = await self.return_tasks_with_status(status)
        result = ''
        status_name = {
            2: "Started", 6: "Aborted", 7: "Successs", 8: "Failed"
        }
        for record in tasks:
            formatted_time = record['StartTime'].strftime('%Y-%m-%d %H:%M:%S')
            time_obj = datetime.strptime(formatted_time, '%Y-%m-%d %H:%M:%S')
            new_time_obj = time_obj + timedelta(hours=3)  # Добавление 3 часов
            formatted_time = new_time_obj.strftime('%Y-%m-%d %H:%M:%S')
            duration_seconds = record['duration_seconds'] - 10800  # 10800с = 3часа (разница из-за UTC)
            hours, remainder = divmod(duration_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_duration = f"{str(int(hours)).zfill(2)}:{str(int(minutes)).zfill(2)}:{str(int(seconds)).zfill(2)}"
            result += f"\nID: <code>{record['ID']}</code>" \
                      f"\nApp Name: <b>{record['app_name']}</b>" \
                      f"\nDuration: {formatted_duration}" \
                      f"\nStatus: {status_name[status]}" \
                      f"\nStart Time: {formatted_time}" \
                      f"\n---\n"
        return result


class DataBaseCPU(DataBase):
    def __init__(self, db_name, user, password, host='localhost', port=5432):
        super().__init__(db_name, user, password, host, port)

    async def return_cpu_or_memory_ttk(self, count, meaning):
        return await self.execute_query(
            f"""
        select
        h.host as Сервер,
        ROUND(CAST(hu.value AS NUMERIC), 2) as "Последнее_значение",
        to_timestamp(hu.clock) as "Время_проверки",
        case when hu.clock >= EXTRACT(EPOCH FROM NOW() - INTERVAL '15 minutes') then '<15' end as "15m",
        round(cast(AVG(hu.value) OVER (ORDER BY hu.clock ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) as numeric), 2) AS "Среднее_значение",
        round(cast(MAX(hu.value) OVER (ORDER BY hu.clock ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) as numeric), 2) AS "Максимальное_значение",
        round(cast(MIN(hu.value) OVER (ORDER BY hu.clock ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) as numeric), 2) AS "Минимальное_значение"
    from
        history  hu
        left join items i on i.itemid = hu.itemid 
        left join hosts h on i.hostid = h.hostid
    where  
        hu.clock > EXTRACT(EPOCH FROM NOW() - INTERVAL '24 hours')
        and h.description like '%qlik01%' 
        and i.name like '%{meaning} util%'
    group by 
        h.host, 
        hu.value, 
        hu.clock
    ORDER BY
        "Время_проверки" DESC, -- Сортировка по "Время_проверки" в порядке убывания
        "Сервер" ASC -- Затем по "Сервер" в порядке возрастания
        FETCH FIRST $1 ROW ONLY;
    ;
            """, (count)
        )

    async def return_cpu_or_memory_dev(self, count, meaning):
        return await self.execute_query(
            f"""
        select
        h.host as Сервер,
        ROUND(CAST(hu.value AS NUMERIC), 2) as "Последнее_значение",
        to_timestamp(hu.clock) as "Время_проверки",
        case when hu.clock >= EXTRACT(EPOCH FROM NOW() - INTERVAL '15 minutes') then '<15' end as "15m",
        round(cast(AVG(hu.value) OVER (ORDER BY hu.clock ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) as numeric), 2) AS "Среднее_значение",
        round(cast(MAX(hu.value) OVER (ORDER BY hu.clock ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) as numeric), 2) AS "Максимальное_значение",
        round(cast(MIN(hu.value) OVER (ORDER BY hu.clock ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) as numeric), 2) AS "Минимальное_значение"
    from
        history  hu
        left join items i on i.itemid = hu.itemid 
        left join hosts h on i.hostid = h.hostid
    where  
        hu.clock > EXTRACT(EPOCH FROM NOW() - INTERVAL '24 hours')
        and h.description like '%qlik02%' 
        and i.name like '%{meaning} util%'
    group by 
        h.host, 
        hu.value, 
        hu.clock
    ORDER BY
        "Время_проверки" DESC, -- Сортировка по "Время_проверки" в порядке убывания
        "Сервер" ASC -- Затем по "Сервер" в порядке возрастания
        FETCH FIRST $1 ROW ONLY;
    ;
            """, count
        )

    async def return_cpu_or_memory_pl(self, count, meaning):
        return await self.execute_query(
            f"""
        select
        h.host as Сервер,
        ROUND(CAST(hu.value AS NUMERIC), 2) as "Последнее_значение",
        to_timestamp(hu.clock) as "Время_проверки",
        case when hu.clock >= EXTRACT(EPOCH FROM NOW() - INTERVAL '15 minutes') then '<15' end as "15m",
        round(cast(AVG(hu.value) OVER (ORDER BY hu.clock ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) as numeric), 2) AS "Среднее_значение",
        round(cast(MAX(hu.value) OVER (ORDER BY hu.clock ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) as numeric), 2) AS "Максимальное_значение",
        round(cast(MIN(hu.value) OVER (ORDER BY hu.clock ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) as numeric), 2) AS "Минимальное_значение"
    from
        history  hu
        left join items i on i.itemid = hu.itemid 
        left join hosts h on i.hostid = h.hostid
    where  
        hu.clock > EXTRACT(EPOCH FROM NOW() - INTERVAL '24 hours')
        and h.description like '%qlik03%' 
        and i.name like '%%{meaning} util%'
    group by 
        h.host, 
        hu.value, 
        hu.clock
    ORDER BY
        "Время_проверки" DESC, -- Сортировка по "Время_проверки" в порядке убывания
        "Сервер" ASC -- Затем по "Сервер" в порядке возрастания
        FETCH FIRST $1 ROW ONLY;
    ;
            """, count
        )


if __name__ == '__main__':
    async def main():
        db = DataBase('QSR', 'tat100yakvv', 'qwer1234', "10.19.63.2")
        await db.connect()
        tasks = await db.get_tasks(2)
        print(tasks)
        await db.close()

    asyncio.run(main())
