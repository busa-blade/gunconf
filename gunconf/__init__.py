import gettext
import logging
import os


version_info = (0, 3, 0, 'rc2')
__version__ = '%d.%d.%d%s' % version_info

aimtrak_version_info = (9, 19)


gettext.install('gettext_example', 'locale', names=['ngettext'])

def logTo(fileNm=None, level=logging.WARNING):
    """ set log format and output """
    # reset other handlers
    #    logging.root.handlers = []

    fmt='%(levelname)-7s | %(asctime)-23s | %(name)-8s | %(message)s'
    logging.basicConfig(format=fmt, filename=fileNm,
                        filemode='w', level=level)

# set a default logging level if none is set
if len(logging.root.handlers) == 0:
    lvlVar = os.getenv('GCF_LOG_LEVEL')
    if not (lvlVar == None):
        print(f"Logging level is set to '{lvlVar}'")
    level = logging.WARNING
    if 'debug' == lvlVar:
        level = logging.DEBUG
    elif 'info' == lvlVar:
        level = logging.INFO

    flVar = os.getenv('GCF_LOG_FILE')
    if not (flVar == None):
        print (f"Logging output to file {flVar}")

    logTo(fileNm=flVar, level=level)
