# coding=UTF8
# import mysqldb
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql://root:@localhost:3306/news?charset=utf8')  # 建立连接
Base = declarative_base()  # 调用基类
Session = sessionmaker(bind=engine)  # 创建 Session


# 定义类
class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String(2000), nullable=False)
    types = Column(String(10), nullable=False)
    image = Column(String(300), )
    author = Column(String(20), )
    view_count = Column(Integer)
    created_at = Column(DateTime)
    is_valid = Column(Boolean)


class OrmTest(object):
    def __init__(self):
        self.session = Session()

    def add_one(self):
        """ 新增记录 """
        new_obj = News(
            title='标题',
            content='内容',
            types='百家',
        )
        try:
            self.session.add(new_obj)
            self.session.commit()
            return new_obj
        except Exception as err:
            self.session.rollback()
            print(err)

    def add_two(self):
        """ 插入多条数据用 session.add_all([list])"""
        new_obj = News(
            title='标题',
            content='内容',
            types='百家',
        )
        new_obj2 = News(
            title='标题',
            content='内容',
            types='百家',
        )
        self.session.add(new_obj)
        self.session.add(new_obj2)
        self.session.commit()
        return new_obj

    def get_one(self):
        """ 查询一条数据 """
        return self.session.query(News).get(1)

    def get_more(self):
        """查询多条语句"""
        return self.session.query(News).filter_by(is_valid=1)

    def update_data(self, pk):
        """ 修改单条数据 """
        new_obj = self.session.query(News).get(pk)
        if new_obj:
            try:
                new_obj.is_valid = 0
                self.session.add(new_obj)
                self.session.commit()
                return True
            except Exception as err:
                self.session.rollback()
                print(err)
        return False

    def update_data_more(self):
        """ 修改多条语句 """
        data_list = self.session.query(News).filter_by(is_valid=False)
        if data_list:
            try:
                for item in data_list:
                    item.is_valid = 1
                    self.session.add(item)
                self.session.commit()
                return True
            except Exception as err:
                self.session.rollback()
                print(err)
        return False

    def delete_data(self, pk):
        """ 删除单条数据"""
        # 获取要删除的数据
        try:
            new_obj = self.session.query(News).get(pk)
            self.session.delete(new_obj)
            self.session.commit()
            return True
        except Exception as err:
            self.session.rollback()
            print(err)
        return False

    def delete_data_more(self, list_pk):
        """ 删除多条数据 """  """有点问题没解决"""
        # 获取要删除的数据
        data_list = self.session.query(News).filter(News.id.in_(list_pk))
        if data_list:
            try:
                for item in data_list:
                    self.session.delete(item)
                self.session.commit()
                return True
            except Exception as err:
                self.session.rollback()
                print(err)
        return False





def main():
    obj = OrmTest()
    # rest = obj.add_one()
    # rest2 = obj.add_two()
    # print(rest.id)
    # print(rest2.id)

    # rest = obj.get_one()
    # if rest:
    #     print('ID:{0}=> {1}'.format(rest.id, rest.title))
    # else:
    #     print('Not exist.')

    # rest = obj.get_more()
    # print(rest.count())
    # if rest:
    #     for new_obj in rest:
    #         print('ID:{0}=> {1}'.format(new_obj.id, new_obj.title))
    # else:
    #     print("Not exits.")

    # print(obj.update_data(2))
    # print(obj.update_data_more())

    print(obj.delete_data(1))
    print(obj.delete_data_more([2,3]))


if __name__ == '__main__':
    main()

















