from discord.ext import commands
from .db import DB

async def setup_commands(bot):
    db = DB()
    await db.create_table()  # Убедимся, что таблицы существуют

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def add(ctx, *, task_desc):
        await db.add_task(ctx.author.id, task_desc)  # Добавил await
        await ctx.send(f"Task added: {task_desc}")

    @bot.command()
    async def list(ctx):
        tasks = await db.get_tasks(ctx.author.id)  # Добавил await
        if not tasks:
            await ctx.send("У вас нет задач!")
            return
        response = '\n'.join([f"{t[0]}: {t[2]} ({'✓' if t[3] else '✗'})" for t in tasks])
        await ctx.send(response)

    @bot.command()
    async def done(ctx, task_id: str):
        if not task_id.isdigit():
            await ctx.send("Ошибка: ID задачи должен быть целым числом.")
            return
        task_id = int(task_id)
        if await db.update_task_status(ctx.author.id, task_id, True):  # Добавил await
            await ctx.send(f"Задача {task_id} выполнена!")
        else:
            await ctx.send(f"Ошибка: Задача {task_id} не найдена.")

    @bot.command()
    async def delete(ctx, task_id: str):
        if not task_id.isdigit():
            await ctx.send("Ошибка: ID задачи должен быть целым числом.")
            return
        task_id = int(task_id)
        if await db.delete_task(ctx.author.id, task_id):  # Добавил await
            await ctx.send(f"Задача {task_id} удалена!")
        else:
            await ctx.send(f"Ошибка: Задача {task_id} не найдена.")

    @bot.command()
    async def help(ctx):
        help_text = (
            "**Доступные команды:**\n"
            "`!add <описание>` — добавить новую задачу.\n"
            "`!list` — показать все задачи.\n"
            "`!done <номер>` — отметить задачу как выполненную.\n"
            "`!delete <номер>` — удалить задачу.\n"
            "`!help` — показать список команд."
        )
        await ctx.send(help_text)
