from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category,News

async def get_categories(db: AsyncSession,sikp:int=0,limit:int=100):
    stmt = select(Category).offset(sikp).limit(limit)
    result= await db.execute(stmt)
    return result.scalars().all()



async def get_news_list(db: AsyncSession, category_id:int, sikp:int=0, limit:int=10):
    #查询的是指定分类下的所有新闻
    stmt = select(News).where(News.category_id == category_id).offset(sikp).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_news_count(db: AsyncSession, category_id:int):
    #查询的是指定分类下的新闻数量
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one() #只能有一个结果，要是0个或者多个就会报错


async def get_news_detail(db: AsyncSession,  news_id:int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()