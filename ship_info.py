import uuid

class ShipInfo:
    
    def __init__(self, ip=None, port=None, com=None, connect_type=None) -> None:
        self.id = str(uuid.uuid1())
        self.ip = ip
        self.port = port
        self.com = com
        self.connect_type = connect_type
        
    def is_ship(self, addr) -> bool:
        if addr[0] == self.ip and addr[1] == self.port:
            return True
        else:
            return False
    def get_ship_info(self):
        temp = {
            'id': self.id
        }
        return temp