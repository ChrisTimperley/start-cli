import logging

from cement.core.foundation import CementApp
from cement.ext.ext_argparse import ArgparseController

try:
    from .repair import RepairController
except Exception:
    pass

from .test import TestController
from .image import ImageController



BANNER = """

          _____                _____                    _____                    _____                _____          
         /\    \              /\    \                  /\    \                  /\    \              /\    \         
        /::\    \            /::\    \                /::\    \                /::\    \            /::\    \        
       /::::\    \           \:::\    \              /::::\    \              /::::\    \           \:::\    \       
      /::::::\    \           \:::\    \            /::::::\    \            /::::::\    \           \:::\    \      
     /:::/\:::\    \           \:::\    \          /:::/\:::\    \          /:::/\:::\    \           \:::\    \     
    /:::/__\:::\    \           \:::\    \        /:::/__\:::\    \        /:::/__\:::\    \           \:::\    \    
    \:::\   \:::\    \          /::::\    \      /::::\   \:::\    \      /::::\   \:::\    \          /::::\    \   
  ___\:::\   \:::\    \        /::::::\    \    /::::::\   \:::\    \    /::::::\   \:::\    \        /::::::\    \  
 /\   \:::\   \:::\    \      /:::/\:::\    \  /:::/\:::\   \:::\    \  /:::/\:::\   \:::\____\      /:::/\:::\    \ 
/::\   \:::\   \:::\____\    /:::/  \:::\____\/:::/  \:::\   \:::\____\/:::/  \:::\   \:::|    |    /:::/  \:::\____\
\:::\   \:::\   \::/    /   /:::/    \::/    /\::/    \:::\  /:::/    /\::/   |::::\  /:::|____|   /:::/    \::/    /
 \:::\   \:::\   \/____/   /:::/    / \/____/  \/____/ \:::\/:::/    /  \/____|:::::\/:::/    /   /:::/    / \/____/ 
  \:::\   \:::\    \      /:::/    /                    \::::::/    /         |:::::::::/    /   /:::/    /          
   \:::\   \:::\____\    /:::/    /                      \::::/    /          |::|\::::/    /   /:::/    /           
    \:::\  /:::/    /    \::/    /                       /:::/    /           |::| \::/____/    \::/    /            
     \:::\/:::/    /      \/____/                       /:::/    /            |::|  ~|           \/____/             
      \::::::/    /                                    /:::/    /             |::|   |                               
       \::::/    /                                    /:::/    /              \::|   |                               
        \::/    /                                     \::/    /                \:|   |                               
         \/____/                                       \/____/                  \|___|                               
                                                                                                                     
"""


class BaseController(ArgparseController):
    class Meta:
        label = 'base'
        description = 'A command-line interface to START.'
        arguments = [
            (['--version'], {'action': 'version',
                             'version': BANNER}),
            (['--verbose'], {'action': 'store_true',
                             'help': 'enables detailed reporting.'})
        ]

    def default(self):
        # type: () -> None
        self.app.args.print_help()


class CLI(CementApp):
    class Meta:
        label = 'start'
        base_controller = BaseController
        handlers = [
            TestController,
            ImageController
        ]
        try:
            handlers.append(RepairController)
        except Exception:
            pass


def main():
    with CLI() as app:
        app.run()
