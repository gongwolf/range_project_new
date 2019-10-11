# %%
import web
import datetime

# %%
urls = ('/.*', 'hooks')

app = web.application(urls, globals())


class hooks:
    def POST(self):
        data = web.data()
        print(datetime.datetime.now())
        print('DATA RECEIVED:')
        print(data)
        print
        return 'OK'


if __name__ == '__main__':
    app.run()
#%%
