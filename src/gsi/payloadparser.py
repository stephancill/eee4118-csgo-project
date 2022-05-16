from . import gamestate

class PayloadParser:
    def parse_payload(self, payload, gamestate):
        gamestate.payload = payload
        for item in payload:
            for i in payload[item]:
                try:
                    setattr(getattr(gamestate, item), i, payload[item][i])
                except:
                    pass
