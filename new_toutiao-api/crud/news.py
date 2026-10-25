from sqlalchemy import select, func, update
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

#增加新闻浏览量
async def increase_news_views(db: AsyncSession,news_id:int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    #更新 -> 检查数据库是否真的命中了数据 -> 命中了返回True
    return result.rowcount>0  #rowcount命中行数



#获取相关新闻推荐
async def get_related_news(db: AsyncSession, category_id:int, news_id:int,limit:int=5):
    #order_by -> 浏览量和发布时间
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id
    ).order_by(
        News.views.desc(), #默认是升序，desc表示降序
        News.publish_time.desc()
    ).limit(limit)
    result = await db.execute(stmt)
    # return result.scalars().all()
    related_news = result.scalars().all()
    #列表推导式 推导出新闻的核心数据，然后再return
    return [{
        "id": news_detail.id,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time,
        "categoryId": news_detail.category_id,
        "views": news_detail.views,
    }for news_detail in related_news]