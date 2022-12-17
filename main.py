import utils
import os

source = utils.Source()
source.login(os.environ.get('user'), os.environ.get('password'))
for model in ['Model 3', 'Model X', 'Model Y']:
    source.start_crawl(model)
