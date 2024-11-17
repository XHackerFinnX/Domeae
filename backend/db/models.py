from datetime import datetime, timedelta
import asyncio
import calendar

async def time_completion_date(case_id: str, num_case_id: int, func, func2, func3):

    text_comp = await func(case_id, num_case_id)
    
    if text_comp == []:
        return
    
    date_comp: datetime = text_comp[0][1]
    date_d = date_comp.day
    date_m = date_comp.month
    date_y = date_comp.year
    
    if text_comp[0][0] == 'Сегодня':
    
        new_date_comp = (datetime(date_y, date_m, date_d) - timedelta(minutes=1)) + timedelta(days=1)
        time_today = (new_date_comp - date_comp).total_seconds()

        for i in reversed(range(int(time_today))):
            
            text_comp = await func(case_id, num_case_id)
            
            if text_comp == []:
                return
            
            if text_comp[0][0] in ['Нет', 'Завтра', 'На выходных', 'На следующих выходных']:
                break

            await asyncio.sleep(1)
            
        else:
            print('ok Сегодня')
            await func2(case_id, num_case_id)
            
    elif text_comp[0][0] == 'Завтра':
    
        new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=1, hours=23, minutes=59)
        time_tomorrow = (new_date_comp - date_comp).total_seconds()

        for i in reversed(range(int(time_tomorrow))):
            
            text_comp = await func(case_id, num_case_id)
            
            if text_comp == []:
                return

            if text_comp[0][0] in ['Нет', 'Сегодня', 'На выходных', 'На следующих выходных']:
                break
            
            date_c = datetime.now()
            
            date_c = datetime(year=date_c.year, month=date_c.month, day=date_c.day)
            date_today_comp = datetime(year=new_date_comp.year, month=new_date_comp.month, day=new_date_comp.day)

            if date_c == date_today_comp:
                
                await func3(case_id, num_case_id, 'Сегодня')
                
                try:
                    _ = asyncio.run(await main_completion_date(case_id, num_case_id, func, func2, func3))
                except:
                    pass
                
                break

            await asyncio.sleep(1)
            
        else:
            print('ok Завтра')
            await func2(case_id, num_case_id)
            
    elif text_comp[0][0] == 'На выходных':
        
        num_week = calendar.weekday(date_y, date_m, date_d)
        
        for i, name in enumerate(calendar.day_abbr):
            if i == num_week:
                name_week = name
                break
            
        if name_week == 'Mon':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=6, hours=23, minutes=59)
            
        elif name_week == 'Tue':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=5, hours=23, minutes=59)
            
        elif name_week == 'Wed':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=4, hours=23, minutes=59)
            
        elif name_week == 'Thu':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=3, hours=23, minutes=59)
            
        elif name_week == 'Fri':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=3, hours=23, minutes=59)
            
        elif name_week == 'Sat':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=1, hours=23, minutes=59)
            
        elif name_week == 'Sun':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(hours=23, minutes=59)

        time_weekend = (new_date_comp - date_comp).total_seconds()
        
        for i in reversed(range(int(time_weekend))):
            
            text_comp = await func(case_id, num_case_id)
            
            if text_comp == []:
                return

            if text_comp[0][0] in ['Нет', 'Завтра', 'Сегодня', 'На следующих выходных']:
                break
            
            date_c = datetime.now()
            
            date_c = datetime(year=date_c.year, month=date_c.month, day=date_c.day)
            date_tomorrow_comp = datetime(year=new_date_comp.year, month=new_date_comp.month, day=new_date_comp.day)

            if date_c + timedelta(days=1) == date_tomorrow_comp:
                
                await func3(case_id, num_case_id, 'Завтра')
                
                try:
                    _ = asyncio.run(await main_completion_date(case_id, num_case_id, func, func2, func3))
                except:
                    pass
                
                break
            
            await asyncio.sleep(1)
            
        else:
            print('ok На выходных')
            await func2(case_id, num_case_id)
            
    elif text_comp[0][0] == 'На следующих выходных':
        
        num_week = calendar.weekday(date_y, date_m, date_d)
        
        for i, name in enumerate(calendar.day_abbr):
            if i == num_week:
                name_week = name
                break
            
        if name_week == 'Mon':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=7, hours=23, minutes=59)
            
        elif name_week == 'Tue':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=6, hours=23, minutes=59)
            
        elif name_week == 'Wed':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=5, hours=23, minutes=59)
            
        elif name_week == 'Thu':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=4, hours=23, minutes=59)
            
        elif name_week == 'Fri':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=3, hours=23, minutes=59)
            
        elif name_week == 'Sat':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=2, hours=23, minutes=59)
            
        elif name_week == 'Sun':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=1, hours=23, minutes=59)

        time_next_weekend = (new_date_comp - date_comp).total_seconds()

        for i in reversed(range(int(time_next_weekend))):
            
            text_comp = await func(case_id, num_case_id)
            
            if text_comp == []:
                return
            
            if text_comp[0][0] in ['Нет', 'Завтра', 'Сегодня', 'На выходных']:
                break
            
            date_c = datetime.now()
            
            date_c = datetime(year=date_c.year, month=date_c.month, day=date_c.day)
            date_weekend_comp = datetime(year=new_date_comp.year, month=new_date_comp.month, day=new_date_comp.day)
 
            if date_c == date_weekend_comp:
                
                await func3(case_id, num_case_id, 'На выходных')
                
                try:
                    _ = asyncio.run(await main_completion_date(case_id, num_case_id, func, func2, func3))
                except:
                    pass
                
                break
            
            await asyncio.sleep(1)
            
        else:
            print('ok На следующих выходных')
            await func2(case_id, num_case_id)
            
    return


async def time_completion_date_store(case_id: str, num_case_id: int, func, func2, func3):

    text_comp = await func(case_id, num_case_id)
    
    if text_comp == []:
        return
    
    date_comp: datetime = text_comp[0][1]
    date_d = date_comp.day
    date_m = date_comp.month
    date_y = date_comp.year
    
    if text_comp[0][0] == 'Сегодня':
    
        new_date_comp = (datetime(date_y, date_m, date_d) - timedelta(minutes=1)) + timedelta(days=1)
        time_today = (new_date_comp - date_comp).total_seconds()

        for i in reversed(range(int(time_today))):
            
            text_comp = await func(case_id, num_case_id)
            
            if text_comp == []:
                return
            
            if text_comp[0][0] in ['Нет', 'Завтра', 'На выходных', 'На следующих выходных']:
                break

            await asyncio.sleep(1)
            
        else:
            print('ok Сегодня')
            await func2(case_id, num_case_id)
            
    elif text_comp[0][0] == 'Завтра':
    
        new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=1, hours=23, minutes=59)
        time_tomorrow = (new_date_comp - date_comp).total_seconds()

        for i in reversed(range(int(time_tomorrow))):
            
            text_comp = await func(case_id, num_case_id)
            
            if text_comp == []:
                return

            if text_comp[0][0] in ['Нет', 'Сегодня', 'На выходных', 'На следующих выходных']:
                break
            
            date_c = datetime.now()
            
            date_c = datetime(year=date_c.year, month=date_c.month, day=date_c.day)
            date_today_comp = datetime(year=new_date_comp.year, month=new_date_comp.month, day=new_date_comp.day)

            if date_c == date_today_comp:
                
                await func3(case_id, num_case_id, 'Сегодня')
                
                try:
                    _ = asyncio.run(await main_completion_date_store(case_id, num_case_id, func, func2, func3))
                except:
                    pass
                
                break

            await asyncio.sleep(1)
            
        else:
            print('ok Завтра')
            await func2(case_id, num_case_id)
            
    elif text_comp[0][0] == 'На выходных':
        
        num_week = calendar.weekday(date_y, date_m, date_d)
        
        for i, name in enumerate(calendar.day_abbr):
            if i == num_week:
                name_week = name
                break
            
        if name_week == 'Mon':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=6, hours=23, minutes=59)
            
        elif name_week == 'Tue':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=5, hours=23, minutes=59)
            
        elif name_week == 'Wed':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=4, hours=23, minutes=59)
            
        elif name_week == 'Thu':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=3, hours=23, minutes=59)
            
        elif name_week == 'Fri':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=3, hours=23, minutes=59)
            
        elif name_week == 'Sat':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=1, hours=23, minutes=59)
            
        elif name_week == 'Sun':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(hours=23, minutes=59)

        time_weekend = (new_date_comp - date_comp).total_seconds()
        
        for i in reversed(range(int(time_weekend))):
            
            text_comp = await func(case_id, num_case_id)
            
            if text_comp == []:
                return

            if text_comp[0][0] in ['Нет', 'Завтра', 'Сегодня', 'На следующих выходных']:
                break
            
            date_c = datetime.now()
            
            date_c = datetime(year=date_c.year, month=date_c.month, day=date_c.day)
            date_tomorrow_comp = datetime(year=new_date_comp.year, month=new_date_comp.month, day=new_date_comp.day)

            if date_c + timedelta(days=1) == date_tomorrow_comp:
                
                await func3(case_id, num_case_id, 'Завтра')
                
                try:
                    _ = asyncio.run(await main_completion_date_store(case_id, num_case_id, func, func2, func3))
                except:
                    pass
                
                break
            
            await asyncio.sleep(1)
            
        else:
            print('ok На выходных')
            await func2(case_id, num_case_id)
            
    elif text_comp[0][0] == 'На следующих выходных':
        
        num_week = calendar.weekday(date_y, date_m, date_d)
        
        for i, name in enumerate(calendar.day_abbr):
            if i == num_week:
                name_week = name
                break
            
        if name_week == 'Mon':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=7, hours=23, minutes=59)
            
        elif name_week == 'Tue':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=6, hours=23, minutes=59)
            
        elif name_week == 'Wed':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=5, hours=23, minutes=59)
            
        elif name_week == 'Thu':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=4, hours=23, minutes=59)
            
        elif name_week == 'Fri':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=3, hours=23, minutes=59)
            
        elif name_week == 'Sat':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=2, hours=23, minutes=59)
            
        elif name_week == 'Sun':
            new_date_comp = datetime(date_y, date_m, date_d) + timedelta(days=1, hours=23, minutes=59)

        time_next_weekend = (new_date_comp - date_comp).total_seconds()

        for i in reversed(range(int(time_next_weekend))):
            
            text_comp = await func(case_id, num_case_id)
            
            if text_comp == []:
                return
            
            if text_comp[0][0] in ['Нет', 'Завтра', 'Сегодня', 'На выходных']:
                break
            
            date_c = datetime.now()
            
            date_c = datetime(year=date_c.year, month=date_c.month, day=date_c.day)
            date_weekend_comp = datetime(year=new_date_comp.year, month=new_date_comp.month, day=new_date_comp.day)
 
            if date_c == date_weekend_comp:
                
                await func3(case_id, num_case_id, 'На выходных')
                
                try:
                    _ = asyncio.run(await main_completion_date_store(case_id, num_case_id, func, func2, func3))
                except:
                    pass
                
                break
            
            await asyncio.sleep(1)
            
        else:
            print('ok На следующих выходных')
            await func2(case_id, num_case_id)
            
    return


async def main_completion_date(case_id: str, num_case_id: int, func, func2, func3):
    
    _ = asyncio.create_task(time_completion_date(case_id, num_case_id, func, func2, func3))
    
    return

async def main_completion_date_store(case_id: str, num_case_id: int, func, func2, func3):
    
    _ = asyncio.create_task(time_completion_date_store(case_id, num_case_id, func, func2, func3))
    
    return