from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import itertools
import numpy


author = 'UEC'

doc = """
Markets
"""


class Constants(BaseConstants):
    name_in_url = 'app_1_market'
    players_per_group = 4
    num_rounds = 5
    endowment = 3
    see_list_cost = 0.3

    packages = [i for i in range(1, 6)]
    id = itertools.cycle([i for i in range(1,11)])

    seller_valuations = [7, 6, 5, 5, 4, 4, 3, 2, 1, 1]
    buyer_valuations = [10, 10, 9, 8, 8, 7, 6, 6, 5, 4]

    com_practice = [i for i in range(1,5)]

    instructions_template ='app_1_market/instructions.html'


class Subsession(BaseSubsession):

    def creating_session(self):
        #crear roles
            if self.round_number == 1:
                    roles = itertools.cycle(['seller', 'buyer'])
                    for p in self.get_players():
                        p.participant.vars['role'] = next(roles)

        #Esto le asigna a los jugadores desde la primera ronda el role de vededor o de comprador
        #assign packages con replacement
            for p in self.get_players():
                if p.participant.vars['role'] == 'seller':
                    p.seller_package = numpy.random.randint(1, 5)
                    p.participant.vars['seller_package'] = p.seller_package
                    p.seller_valuation = numpy.random.choice(Constants.seller_valuations, replace=False)
                    p.seller_id = next(Constants.id)
                    #todo have to fix this id. They don't work as I would like it to
                    p.participant.vars['seller_id'] = p.seller_id #assign a seller id

                else:
            # Assign valuations for each packaque for the sellers
            #Esta parte del código debería asignarle un valor random a cada paquete
                    p.participant.vars["valuations"] = dict(zip(Constants.packages, numpy.random.choice(Constants.buyer_valuations, size =5, replace = False)))
                    p.buyer_valuation_pac1 = p.participant.vars["valuations"].get(1)
                    p.buyer_valuation_pac2 = p.participant.vars["valuations"].get(2)
                    p.buyer_valuation_pac3 = p.participant.vars["valuations"].get(3)
                    p.buyer_valuation_pac4 = p.participant.vars["valuations"].get(4)
                    p.buyer_valuation_pac5 = p.participant.vars["valuations"].get(5)
                #todo fix this id. They don't work as it should
                    p.participant.vars['buyer_id'] = next(Constants.id)



class Group(BaseGroup):

    #Acá calcular los resultados de la ronda para los pagos tengo el id del vendedor, a partir de eso
    #debo recuperar qué vendió y a cómo
    def set_payoff(self):

        for p in self.get_players():
            if p.role() == "buyer":
                the_seller = self.get_player_by_id(p.my_seller)

                #get info of the package
                p.package_purchased = the_seller.seller_package
                p.paid = the_seller.ask_price_fin
                p.payoff = p.participant.vars['valuations'].get(p.package_purchased) - p.paid
            else:

                p.payoff = p.ask_price_fin - p.seller_valuation - int(p.see_list)*Constants.see_list_cost
                #todo if he is not purchased, then he earns nothing!
                #todo agregar una dummy de si fue purcheseado o no.

class Player(BasePlayer):

    def role(self):
        if self.participant.vars['role'] == 'buyer':
            return 'buyer'
        else:
            return 'seller'

    #Seller
    seller_package = models.IntegerField()
    seller_valuation = models.IntegerField()
    ask_price_ini = models.IntegerField()
    see_list = models.BooleanField(initial = False)
    com_practice = models.IntegerField(choices = [1, 2, 3, 4])
    ask_price_fin = models.IntegerField()
    seller_id = models.IntegerField()
    purchased = models.BooleanField()

    #Buyer
    #Preguntar a Felipe si puedo borrar estos campos de valuación de cada paquete
    buyer_valuation_pac1 = models.IntegerField()
    buyer_valuation_pac2 = models.IntegerField()
    buyer_valuation_pac3 = models.IntegerField()
    buyer_valuation_pac4 = models.IntegerField()
    buyer_valuation_pac5 = models.IntegerField()
    bid_price = models.IntegerField()
    package_purchased = models.IntegerField()
    my_seller = models.IntegerField()
    paid = models.IntegerField()
    buyer_id = models.IntegerField()
