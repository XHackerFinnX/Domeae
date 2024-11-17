import psycopg2
from psycopg2 import Error, InterfaceError
from core.config import config

from collections import namedtuple

from datetime import datetime

class DataBaseHome:
    def __init__(self):
        self._connection = None

    def _connect(self):
        if not self._connection or self._connection.closed:
            self._connection = psycopg2.connect(
                host=config.POSTGRESQL_HOST.get_secret_value(),
                database=config.POSTGRESQL_DATABASE.get_secret_value(),
                user=config.POSTGRESQL_USER.get_secret_value(),
                password=config.POSTGRESQL_PASSWORD.get_secret_value(),
                port=config.POSTGRESQL_PORT.get_secret_value()
            )
        return self._connection

    async def insert_home_task(
        self,
        user_id: int,
        case_id: str,
        num_case_id: int,
        case_text: str,
        text_task: str,
        user_name: str,
        completion_date: str,
        priority: bool,
        reminder: int,
        checkbox: bool,
        date_create: datetime
    ):
        query = """
            INSERT INTO public.house_case (
                user_id,
                case_id,
                num_case_id,
                case_text,
                text_task,
                user_name,
                completion_date,
                priority,
                reminder,
                checkbox,
                date_create
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            user_id,
            case_id,
            num_case_id,
            case_text,
            text_task,
            user_name,
            completion_date,
            priority,
            reminder,
            checkbox,
            date_create
        )
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, values)
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка добавления задачи {case_id}, номер: {num_case_id} - {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def case_id_home(
        self,
        case_id: str,
    ):
        
        query = f"""
            SELECT MAX(num_case_id) AS max_case_id
            FROM public.house_case
            WHERE case_id = '{case_id}' AND checkbox = false
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    max_case_id = cursor.fetchall()[0][0]
                    
                    if max_case_id is None:
                        max_case_id = 1
                    else:
                        max_case_id += 1
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка получения максимального {case_id}. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
            return max_case_id
        
    async def update_checkbox_home(self, case_id: str, num_case_id: int):
        
        query = f"""
            UPDATE public.house_case 
            SET checkbox = true
            WHERE case_id = '{case_id}' 
            AND num_case_id = {num_case_id}
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка обновления checkbox {case_id}. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def update_user_name(self, case_id: str, num_case_id: int, user_name: str):
        
        query = f"""
            UPDATE public.house_case
            SET user_name = '{user_name}'
            WHERE case_id = '{case_id}' 
            AND num_case_id = {num_case_id}
            AND checkbox = false
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка обновления username {case_id}. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def update_priority(self, case_id: str, num_case_id: int, priority: bool):
        
        query = f"""
            UPDATE public.house_case
            SET priority = {priority}
            WHERE case_id = '{case_id}' 
            AND num_case_id = {num_case_id}
            AND checkbox = false
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка обновления priority {case_id}. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def delete_task(self, case_id: str, num_case_id: int):
        
        query = f"""
            DELETE FROM public.house_case
            WHERE case_id = '{case_id}' 
            AND num_case_id = {num_case_id}
            AND checkbox = false
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка удаления задачи {case_id}. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def update_completion_date(self, case_id: str, num_case_id: int, completion_date: str):
         
        date_c = datetime.now()

        query = f"""
            UPDATE public.house_case
            SET completion_date = '{completion_date}',
            date_create = '{date_c}'
            WHERE case_id = '{case_id}' 
            AND num_case_id = {num_case_id}
            AND checkbox = false
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка обновления completion_date {case_id}. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def update_case(
        self,
        new_case_id: str,
        new_num_case_id: int,
        old_case_id: str,
        old_num_case_id: int,
        case_text: str
    ):
        
        query = f"""
            UPDATE public.house_case
            SET case_id = '{new_case_id}',
            num_case_id = {new_num_case_id},
            case_text = '{case_text}'
            WHERE case_id = '{old_case_id}' 
            AND num_case_id = {old_num_case_id}
            AND checkbox = false
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка обновления и перемещения case {old_case_id} -> {new_case_id}. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def select_data_home(self, username, filter_name: str):
        
        if filter_name == 'today':
            
            query_urgent = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.house_case
                WHERE checkbox = false
                AND case_id = 'urgent'
                AND completion_date = 'Сегодня'
                ORDER BY num_case_id
            """
            
            query_normal = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.house_case
                WHERE checkbox = false
                AND case_id = 'normal'
                AND completion_date = 'Сегодня'
                ORDER BY num_case_id
            """
            
            query_regular = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.house_case
                WHERE checkbox = false
                AND case_id = 'regular'
                AND completion_date = 'Сегодня'
                ORDER BY num_case_id
            """
            
        elif filter_name == 'priority':
            
            query_urgent = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.house_case
                WHERE checkbox = false
                AND case_id = 'urgent'
                AND priority = true
                ORDER BY num_case_id
            """
            
            query_normal = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.house_case
                WHERE checkbox = false
                AND case_id = 'normal'
                AND priority = true
                ORDER BY num_case_id
            """
            
            query_regular = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.house_case
                WHERE checkbox = false
                AND case_id = 'regular'
                AND priority = true
                ORDER BY num_case_id
            """
            
        elif filter_name == 'user':
            
            query_urgent = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.house_case
                WHERE checkbox = false
                AND case_id = 'urgent'
                AND (user_name = '{username}' OR user_name = 'Суперсемейка')
                ORDER BY num_case_id
            """
            
            query_normal = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.house_case
                WHERE checkbox = false
                AND case_id = 'normal'
                AND (user_name = '{username}' OR user_name = 'Суперсемейка')
                ORDER BY num_case_id
            """
            
            query_regular = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.house_case
                WHERE checkbox = false
                AND case_id = 'regular'
                AND (user_name = '{username}' OR user_name = 'Суперсемейка')
                ORDER BY num_case_id
            """
            
        else:
            
            query_urgent = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.house_case
                WHERE checkbox = false
                AND case_id = 'urgent'
                ORDER BY num_case_id
            """
            
            query_normal = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.house_case
                WHERE checkbox = false
                AND case_id = 'normal'
                ORDER BY num_case_id
            """
            
            query_regular = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.house_case
                WHERE checkbox = false
                AND case_id = 'regular'
                ORDER BY num_case_id
            """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    
                    cursor.execute(query_urgent)
                    data_urgent = cursor.fetchall()
                    
                    cursor.execute(query_normal)
                    data_normal = cursor.fetchall()
                    
                    cursor.execute(query_regular)
                    data_regular = cursor.fetchall()
                    
                    Data = namedtuple('Data', ['urgent', 'normal', 'regular'])
                    
                    data_i = Data(data_urgent, data_normal, data_regular)
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка получения задач для дома. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
                return data_i
            
    async def count_home(self, username: str):
        
        query_priority = """
            SELECT COUNT(priority)
            FROM public.house_case
            WHERE checkbox = false
            AND priority = true
        """
        
        query_checkbox_true = """
            SELECT COUNT(checkbox)
            FROM public.house_case
            WHERE checkbox = true
        """
        
        query_checkbox_false = """
            SELECT COUNT(checkbox)
            FROM public.house_case
            WHERE checkbox = false
        """
        
        query_completion_date = """
            SELECT COUNT(completion_date)
            FROM public.house_case
            WHERE checkbox = false
            AND completion_date = 'Сегодня'
        """
        
        query_user_name = f"""
            SELECT COUNT(user_name)
            FROM public.house_case
            WHERE checkbox = false 
            AND (user_name = '{username}' OR user_name = 'Суперсемейка')
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    
                    cursor.execute(query_priority)
                    count_priority = cursor.fetchall()[0][0]
                    
                    cursor.execute(query_checkbox_true)
                    count_checkbox_true = cursor.fetchall()[0][0]
                    
                    cursor.execute(query_checkbox_false)
                    count_checkbox_false = cursor.fetchall()[0][0]
                    
                    cursor.execute(query_completion_date)
                    count_completion_date = cursor.fetchall()[0][0]
                    
                    cursor.execute(query_user_name)
                    count_user_name = cursor.fetchall()[0][0]
                    
                    Datacount = namedtuple(
                        'Datacount',
                        [
                            'count_priority',
                            'count_checkbox_true',
                            'count_checkbox_false',
                            'count_completion_date',
                            'count_user_name'
                        ]
                    )
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка получения количеста. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
                return Datacount(
                    count_priority,
                    count_checkbox_true,
                    count_checkbox_false,
                    count_completion_date,
                    count_user_name
                )
                
    async def select_completion_date(self, case_id: str, num_case_id: int):
        
        query = f"""
            SELECT completion_date,
            date_create
            FROM public.house_case
            WHERE case_id = '{case_id}'
            AND num_case_id = {num_case_id}
            AND checkbox = false
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    date_comp = cursor.fetchall()
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка получения completion_date для расчета времени {error}")
        finally:
            if self._connection:
                self._connection.close()

                return date_comp


class DataBaseStory:
    def __init__(self):
        self._connection = None

    def _connect(self):
        if not self._connection or self._connection.closed:
            self._connection = psycopg2.connect(
                host=config.POSTGRESQL_HOST.get_secret_value(),
                database=config.POSTGRESQL_DATABASE.get_secret_value(),
                user=config.POSTGRESQL_USER.get_secret_value(),
                password=config.POSTGRESQL_PASSWORD.get_secret_value(),
                port=config.POSTGRESQL_PORT.get_secret_value()
            )
        return self._connection
    
    async def insert_store_task(
        self,
        user_id: int,
        case_id: str,
        num_case_id: int,
        case_text: str,
        text_task: str,
        user_name: str,
        completion_date: str,
        priority: bool,
        reminder: int,
        sum_pay: int,
        checkbox: bool,
        date_create: datetime
    ):
        query = """
            INSERT INTO public.store_case (
                user_id,
                case_id,
                num_case_id,
                case_text,
                text_task,
                user_name,
                completion_date,
                priority,
                reminder,
                sum_pay,
                checkbox,
                date_create
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            user_id,
            case_id,
            num_case_id,
            case_text,
            text_task,
            user_name,
            completion_date,
            priority,
            reminder,
            sum_pay,
            checkbox,
            date_create
        )
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, values)
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка добавления задачи {case_id}, номер: {num_case_id} - {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def case_id_store(
        self,
        case_id: str,
    ):
        
        query = f"""
            SELECT MAX(num_case_id) AS max_case_id
            FROM public.store_case
            WHERE case_id = '{case_id}' AND checkbox = false
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    max_case_id = cursor.fetchall()[0][0]
                    
                    if max_case_id is None:
                        max_case_id = 1
                    else:
                        max_case_id += 1
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка получения максимального {case_id}. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
            return max_case_id
        
    async def update_checkbox_store(self, case_id: str, num_case_id: int, sum_pay: int):
        
        query = f"""
            UPDATE public.store_case
            SET checkbox = true,
            sum_pay = {sum_pay}
            WHERE case_id = '{case_id}' 
            AND num_case_id = {num_case_id}
            AND checkbox = false
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка обновления checkbox {case_id}. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def update_user_name_store(self, case_id: str, num_case_id: int, user_name: str):
        
        query = f"""
            UPDATE public.store_case
            SET user_name = '{user_name}'
            WHERE case_id = '{case_id}' 
            AND num_case_id = {num_case_id}
            AND checkbox = false
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка обновления username {case_id}. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def update_priority_store(self, case_id: str, num_case_id: int, priority: bool):
        
        query = f"""
            UPDATE public.store_case
            SET priority = {priority}
            WHERE case_id = '{case_id}' 
            AND num_case_id = {num_case_id}
            AND checkbox = false
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка обновления priority {case_id}. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def delete_task_store(self, case_id: str, num_case_id: int):
        
        query = f"""
            DELETE FROM public.store_case
            WHERE case_id = '{case_id}' 
            AND num_case_id = {num_case_id}
            AND checkbox = false
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка удаления задачи {case_id}. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def update_completion_date_store(self, case_id: str, num_case_id: int, completion_date: str):
         
        date_c = datetime.now()

        query = f"""
            UPDATE public.store_case
            SET completion_date = '{completion_date}',
            date_create = '{date_c}'
            WHERE case_id = '{case_id}' 
            AND num_case_id = {num_case_id}
            AND checkbox = false
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка обновления completion_date {case_id}. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def update_case_store(
        self,
        new_case_id: str,
        new_num_case_id: int,
        old_case_id: str,
        old_num_case_id: int,
        case_text: str
    ):
        
        query = f"""
            UPDATE public.store_case
            SET case_id = '{new_case_id}',
            num_case_id = {new_num_case_id},
            case_text = '{case_text}'
            WHERE case_id = '{old_case_id}' 
            AND num_case_id = {old_num_case_id}
            AND checkbox = false
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка обновления и перемещения case {old_case_id} -> {new_case_id}. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def select_completion_date_store(self, case_id: str, num_case_id: int):
        
        query = f"""
            SELECT completion_date,
            date_create
            FROM public.store_case
            WHERE case_id = '{case_id}'
            AND num_case_id = {num_case_id}
            AND checkbox = false
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    date_comp = cursor.fetchall()
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка получения completion_date для расчета времени {error}")
        finally:
            if self._connection:
                self._connection.close()

                return date_comp
            
    async def select_data_store(self,username: str, filter_name: str):
        
        if filter_name == 'today':
            
            query_today = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.store_case
                WHERE checkbox = false
                AND case_id = 'today'
                AND completion_date = 'Сегодня'
                ORDER BY num_case_id
            """
            
            query_week = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.store_case
                WHERE checkbox = false
                AND case_id = 'week'
                AND completion_date = 'Сегодня'
                ORDER BY num_case_id
            """
            
            query_month = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.store_case
                WHERE checkbox = false
                AND case_id = 'month'
                AND completion_date = 'Сегодня'
                ORDER BY num_case_id
            """
            
        elif filter_name == 'priority':
            
            query_today = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.store_case
                WHERE checkbox = false
                AND case_id = 'today'
                AND priority = true
                ORDER BY num_case_id
            """
            
            query_week = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.store_case
                WHERE checkbox = false
                AND case_id = 'week'
                AND priority = true
                ORDER BY num_case_id
            """
            
            query_month = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.store_case
                WHERE checkbox = false
                AND case_id = 'month'
                AND priority = true
                ORDER BY num_case_id
            """
            
        elif filter_name == 'user':
            
            query_today = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.store_case
                WHERE checkbox = false
                AND case_id = 'today'
                AND (user_name = '{username}' OR user_name = 'Суперсемейка')
                ORDER BY num_case_id
            """
            
            query_week = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.store_case
                WHERE checkbox = false
                AND case_id = 'week'
                AND (user_name = '{username}' OR user_name = 'Суперсемейка')
                ORDER BY num_case_id
            """
            
            query_month = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.store_case
                WHERE checkbox = false
                AND case_id = 'month'
                AND (user_name = '{username}' OR user_name = 'Суперсемейка')
                ORDER BY num_case_id
            """
            
        else:
            
            query_today = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.store_case
                WHERE checkbox = false
                AND case_id = 'today'
                ORDER BY num_case_id
            """
            
            query_week = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.store_case
                WHERE checkbox = false
                AND case_id = 'week'
                ORDER BY num_case_id
            """
            
            query_month = f"""
                SELECT case_id,
                num_case_id,
                text_task,
                user_name,
                completion_date,
                priority
                FROM public.store_case
                WHERE checkbox = false
                AND case_id = 'month'
                ORDER BY num_case_id
            """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    
                    cursor.execute(query_today)
                    data_today = cursor.fetchall()
                    
                    cursor.execute(query_week)
                    data_week = cursor.fetchall()
                    
                    cursor.execute(query_month)
                    data_month = cursor.fetchall()
                    
                    Data = namedtuple('Data', ['today', 'week', 'month'])
                    
                    data_i = Data(data_today, data_week, data_month)
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка получения задач для покупок. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
                return data_i
            
    async def count_store(self, username: str):
        
        query_priority = """
            SELECT COUNT(priority)
            FROM public.store_case
            WHERE checkbox = false
            AND priority = true
        """
        
        query_checkbox_true = """
            SELECT COUNT(checkbox)
            FROM public.store_case
            WHERE checkbox = true
        """
        
        query_checkbox_false = """
            SELECT COUNT(checkbox)
            FROM public.store_case
            WHERE checkbox = false
        """
        
        query_completion_date = """
            SELECT COUNT(completion_date)
            FROM public.store_case
            WHERE checkbox = false
            AND completion_date = 'Сегодня'
        """
        
        query_user_name = f"""
            SELECT COUNT(user_name)
            FROM public.store_case
            WHERE checkbox = false 
            AND (user_name = '{username}' OR user_name = 'Суперсемейка')
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    
                    cursor.execute(query_priority)
                    count_priority = cursor.fetchall()[0][0]
                    
                    cursor.execute(query_checkbox_true)
                    count_checkbox_true = cursor.fetchall()[0][0]
                    
                    cursor.execute(query_checkbox_false)
                    count_checkbox_false = cursor.fetchall()[0][0]
                    
                    cursor.execute(query_completion_date)
                    count_completion_date = cursor.fetchall()[0][0]
                    
                    cursor.execute(query_user_name)
                    count_user_name = cursor.fetchall()[0][0]
                    
                    Datacount = namedtuple(
                        'Datacount',
                        [
                            'count_priority',
                            'count_checkbox_true',
                            'count_checkbox_false',
                            'count_completion_date',
                            'count_user_name'
                        ]
                    )
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка получения количеста. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
                return Datacount(
                    count_priority,
                    count_checkbox_true,
                    count_checkbox_false,
                    count_completion_date,
                    count_user_name
                )
                
    async def sum_store(self):
        
        date_n = datetime.now()
        
        date_month = date_n.month
        date_year = date_n.year
        
        query = f"""
            SELECT SUM(sum_pay) 
            FROM public.store_case 
            WHERE checkbox = true 
            AND (
	            EXTRACT(MONTHS FROM date_create) = {date_month} 
	            AND EXTRACT(YEARS FROM date_create) = {date_year}
            )
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    date_sum = cursor.fetchall()[0][0]
                    
                    if date_sum is None:
                        date_sum = 0
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка получения суммы {error}")
        finally:
            if self._connection:
                self._connection.close()

                return date_sum
            

class DataBaseStudy:
    def __init__(self):
        self._connection = None

    def _connect(self):
        if not self._connection or self._connection.closed:
            self._connection = psycopg2.connect(
                host=config.POSTGRESQL_HOST.get_secret_value(),
                database=config.POSTGRESQL_DATABASE.get_secret_value(),
                user=config.POSTGRESQL_USER.get_secret_value(),
                password=config.POSTGRESQL_PASSWORD.get_secret_value(),
                port=config.POSTGRESQL_PORT.get_secret_value()
            )
        return self._connection
    
    async def insert_study_task(
        self,
        user_id: int,
        case_id: str,
        num_case_id: int,
        case_text: str,
        text_task: str,
        priority: bool,
        reminder: int,
        checkbox: bool,
        date_create: datetime
    ):
        query = """
            INSERT INTO public.study_case (
                user_id,
                case_id,
                num_case_id,
                case_text,
                text_task,
                priority,
                reminder,
                checkbox,
                date_create
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            user_id,
            case_id,
            num_case_id,
            case_text,
            text_task,
            priority,
            reminder,
            checkbox,
            date_create
        )
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, values)
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка добавления задачи {case_id}, номер: {num_case_id} - {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def case_id_study(
        self,
        case_id: str,
    ):
        
        query = f"""
            SELECT MAX(num_case_id) AS max_case_id
            FROM public.study_case
            WHERE case_id = '{case_id}' AND checkbox = false
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    max_case_id = cursor.fetchall()[0][0]
                    
                    if max_case_id is None:
                        max_case_id = 1
                    else:
                        max_case_id += 1
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка получения максимального {case_id}. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
            return max_case_id
        
    async def update_checkbox_study(self, case_id: str, num_case_id: int):
        
        query = f"""
            UPDATE public.study_case
            SET checkbox = true
            WHERE case_id = '{case_id}' 
            AND num_case_id = {num_case_id}
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка обновления checkbox {case_id}. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def update_priority_study(self, case_id: str, num_case_id: int, priority: bool):
        
        query = f"""
            UPDATE public.study_case
            SET priority = {priority}
            WHERE case_id = '{case_id}' 
            AND num_case_id = {num_case_id}
            AND checkbox = false
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка обновления priority {case_id}. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def delete_task_study(self, case_id: str, num_case_id: int):
        
        query = f"""
            DELETE FROM public.study_case
            WHERE case_id = '{case_id}' 
            AND num_case_id = {num_case_id}
            AND checkbox = false
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка удаления задачи {case_id}. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def select_data_study(self, user_id: int):
        
        query_homework = f"""
            SELECT
            case_id,
            num_case_id,
            text_task,
            priority
            FROM public.study_case
            WHERE checkbox = false
            AND case_id = 'homework'
            AND user_id = {user_id}
            ORDER BY num_case_id
        """
        
        query_exam = f"""
            SELECT
            case_id,
            num_case_id,
            text_task,
            priority
            FROM public.study_case
            WHERE checkbox = false
            AND case_id = 'exam'
            AND user_id = {user_id}
            ORDER BY num_case_id
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    
                    cursor.execute(query_homework)
                    data_homework = cursor.fetchall()
                    
                    cursor.execute(query_exam)
                    data_exam = cursor.fetchall()
                    
                    Data = namedtuple('Data', ['homework', 'exam'])
                    
                    data_i = Data(data_homework, data_exam)
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка получения задач для покупок. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
                return data_i
            
    async def count_study(self, user_id: int):
        
        query_priority = f"""
            SELECT COUNT(priority)
            FROM public.study_case
            WHERE checkbox = false
            AND priority = true
            AND user_id = {user_id}
        """
        
        query_checkbox_true = f"""
            SELECT COUNT(checkbox)
            FROM public.study_case
            WHERE checkbox = true
            AND user_id = {user_id}
        """
        
        query_checkbox_false = f"""
            SELECT COUNT(checkbox)
            FROM public.study_case
            WHERE checkbox = false
            AND user_id = {user_id}
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    
                    cursor.execute(query_priority)
                    count_priority = cursor.fetchall()[0][0]
                    
                    cursor.execute(query_checkbox_true)
                    count_checkbox_true = cursor.fetchall()[0][0]
                    
                    cursor.execute(query_checkbox_false)
                    count_checkbox_false = cursor.fetchall()[0][0]
                    
                    Datacount = namedtuple(
                        'Datacount',
                        [
                            'count_priority',
                            'count_checkbox_true',
                            'count_checkbox_false'
                        ]
                    )
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка получения количеста. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
                return Datacount(
                    count_priority,
                    count_checkbox_true,
                    count_checkbox_false
                )
                

class DataBaseFilter:
    def __init__(self):
        self._connection = None

    def _connect(self):
        if not self._connection or self._connection.closed:
            self._connection = psycopg2.connect(
                host=config.POSTGRESQL_HOST.get_secret_value(),
                database=config.POSTGRESQL_DATABASE.get_secret_value(),
                user=config.POSTGRESQL_USER.get_secret_value(),
                password=config.POSTGRESQL_PASSWORD.get_secret_value(),
                port=config.POSTGRESQL_PORT.get_secret_value()
            )
        return self._connection
    
    async def update_filter(
        self,
        user_id: int,
        filter_name: str
    ):
        query = f"""
            UPDATE public.filter_case 
            SET filter_name = '{filter_name}' 
            WHERE user_id = {user_id}
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка обновления фильтра {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def select_filter(
        self,
        user_id: int
    ):
        query = f"""
            SELECT filter_name 
            FROM public.filter_case
            WHERE user_id = {user_id}
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    f_n = cursor.fetchall()[0][0]
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка получения фильтра {error}")
        finally:
            if self._connection:
                self._connection.close()
                
                return f_n
            
            
class DataBaseCountIndex:
    def __init__(self):
        self._connection = None

    def _connect(self):
        if not self._connection or self._connection.closed:
            self._connection = psycopg2.connect(
                host=config.POSTGRESQL_HOST.get_secret_value(),
                database=config.POSTGRESQL_DATABASE.get_secret_value(),
                user=config.POSTGRESQL_USER.get_secret_value(),
                password=config.POSTGRESQL_PASSWORD.get_secret_value(),
                port=config.POSTGRESQL_PORT.get_secret_value()
            )
        return self._connection
    
    async def select_count_all(self, username: str):
        
        query_priority_store = """
            SELECT COUNT(priority)
            FROM public.store_case
            WHERE checkbox = false
            AND priority = true
        """
        
        query_priority_home = """
            SELECT COUNT(priority)
            FROM public.house_case
            WHERE checkbox = false
            AND priority = true
        """
        
        query_checkbox_true_store = """
            SELECT COUNT(checkbox)
            FROM public.store_case
            WHERE checkbox = true
        """
        
        query_checkbox_true_home = """
            SELECT COUNT(checkbox)
            FROM public.house_case
            WHERE checkbox = true
        """
        
        query_checkbox_false_store = """
            SELECT COUNT(checkbox)
            FROM public.store_case
            WHERE checkbox = false
        """
        
        query_checkbox_false_home = """
            SELECT COUNT(checkbox)
            FROM public.house_case
            WHERE checkbox = false
        """
        
        query_completion_date_store = """
            SELECT COUNT(completion_date)
            FROM public.store_case
            WHERE checkbox = false
            AND completion_date = 'Сегодня'
        """
        
        query_completion_date_home = """
            SELECT COUNT(completion_date)
            FROM public.house_case
            WHERE checkbox = false
            AND completion_date = 'Сегодня'
        """
        
        query_user_name_store = f"""
            SELECT COUNT(user_name)
            FROM public.store_case
            WHERE checkbox = false 
            AND (user_name = '{username}' OR user_name = 'Суперсемейка')
        """
        
        query_user_name_home = f"""
            SELECT COUNT(user_name)
            FROM public.house_case
            WHERE checkbox = false 
            AND (user_name = '{username}' OR user_name = 'Суперсемейка')
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    
                    cursor.execute(query_priority_store)
                    count_priority_store = cursor.fetchall()[0][0]
                    
                    cursor.execute(query_priority_home)
                    count_priority_home = cursor.fetchall()[0][0]
                    
                    cursor.execute(query_checkbox_true_store)
                    count_checkbox_true_store = cursor.fetchall()[0][0]
                    
                    cursor.execute(query_checkbox_true_home)
                    count_checkbox_true_home = cursor.fetchall()[0][0]
                    
                    cursor.execute(query_checkbox_false_store)
                    count_checkbox_false_store = cursor.fetchall()[0][0]
                    
                    cursor.execute(query_checkbox_false_home)
                    count_checkbox_false_home = cursor.fetchall()[0][0]
                    
                    cursor.execute(query_completion_date_store)
                    count_completion_date_store = cursor.fetchall()[0][0]
                    
                    cursor.execute(query_completion_date_home)
                    count_completion_date_home = cursor.fetchall()[0][0]
                    
                    cursor.execute(query_user_name_store)
                    count_user_name_store = cursor.fetchall()[0][0]
                    
                    cursor.execute(query_user_name_home)
                    count_user_name_home = cursor.fetchall()[0][0]
                    
                    Datacount = namedtuple(
                        'Datacount',
                        [
                            'count_priority',
                            'count_checkbox_true',
                            'count_checkbox_false',
                            'count_completion_date',
                            'count_user_name'
                        ]
                    )
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка получения количеста. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
                return Datacount(
                    count_priority_home + count_priority_store,
                    count_checkbox_true_home + count_checkbox_true_store,
                    count_checkbox_false_home + count_checkbox_false_store,
                    count_completion_date_home + count_completion_date_store,
                    count_user_name_home + count_user_name_store
                )
                
                
class DataBasePlan:
    def __init__(self):
        self._connection = None

    def _connect(self):
        if not self._connection or self._connection.closed:
            self._connection = psycopg2.connect(
                host=config.POSTGRESQL_HOST.get_secret_value(),
                database=config.POSTGRESQL_DATABASE.get_secret_value(),
                user=config.POSTGRESQL_USER.get_secret_value(),
                password=config.POSTGRESQL_PASSWORD.get_secret_value(),
                port=config.POSTGRESQL_PORT.get_secret_value()
            )
        return self._connection
    
    async def insert_plan(
        self,
        user_id: int,
        case_id: str,
        num_case_id: int,
        case_text: str,
        text_task: str,
        checkbox: bool,
        date_create: datetime
    ):
        query = """
            INSERT INTO public.plan_case (
                user_id,
                case_id,
                num_case_id,
                case_text,
                text_task,
                checkbox,
                date_create
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            user_id,
            case_id,
            num_case_id,
            case_text,
            text_task,
            checkbox,
            date_create
        )
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, values)
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка добавления плана {case_id}, номер: {num_case_id} - {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def case_id_plan(
        self,
        case_id: str,
    ):
        
        query = f"""
            SELECT MAX(num_case_id) AS max_case_id
            FROM public.plan_case
            WHERE case_id = '{case_id}' AND checkbox = false
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    max_case_id = cursor.fetchall()[0][0]
                    
                    if max_case_id is None:
                        max_case_id = 1
                    else:
                        max_case_id += 1
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка получения максимального {case_id}. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
            return max_case_id
        
    async def delete_plan(self, case_id: str, num_case_id: int):
        
        query = f"""
            DELETE FROM public.plan_case
            WHERE case_id = '{case_id}' 
            AND num_case_id = {num_case_id}
            AND checkbox = false
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка удаления плана {case_id}. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def select_data_plan(self):
            
        query_plan = """
            SELECT case_id,
            num_case_id,
            text_task
            FROM public.plan_case
            WHERE checkbox = false
            AND case_id = 'plan'
            ORDER BY num_case_id
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query_plan)
                    data_plan = cursor.fetchall()
                    
                    Data = namedtuple('Data', ['plan'])
                    
                    data_i = Data(data_plan)
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка получения планов. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
                return data_i
            
    async def update_checkbox_true(self, case_id: str, num_case_id: int):
        
        query = f"""
            UPDATE public.plan_case 
            SET checkbox = true
            WHERE case_id = '{case_id}' 
            AND num_case_id = {num_case_id}
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка обновления checkbox {case_id}. {error}")
        finally:
            if self._connection:
                self._connection.close()
                
    async def select_count_plan(self):
        
        query = """
            SELECT COUNT(case_id) 
            FROM public.plan_case 
            WHERE checkbox = false
        """
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    count_plane = cursor.fetchall()[0][0]
                    
                conn.commit()
        except (InterfaceError, Error) as error:
            print(f"Ошибка получение количества планов {error}")
        finally:
            if self._connection:
                self._connection.close()
                
                return count_plane