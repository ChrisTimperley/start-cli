import logging

from cement.core.foundation import CementApp
from cement.ext.ext_argparse import ArgparseController

from .repair import RepairController
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
            (['--version'], dict(action='version', version=BANNER))
        ]

    def default(self) -> None:
        self.app.args.print_help()


class CLI(CementApp):
    class Meta:
        label = 'start'
        base_controller = BaseController
        handlers = [
            RepairController,
            TestController,
            ImageController
        ]


def main():
    with CLI() as app:
        app.run()
