from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class seller(Page):
    form_model = 'player'
    form_fields = ['ask_price_ini', 'see_list']

    def is_displayed(self):
        return self.player.role() != 'buyer'

    def vars_for_template(self):
        return dict(
            seller_package = self.player.seller_package,
            role = self.participant.vars['role']
        )

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass

class seller_2(Page):
    form_model = 'player'
    form_fields = [
        'com_practice',
        'ask_price_fin'
    ]
    def is_displayed(self):
        return self.player.role() != 'buyer'

    def vars_for_template(self):
        dict(
            role = self.player.role()
        )

class buyer(Page):
    form_model = 'player'
    form_fields = ['bid_price']

    def is_displayed(self):
        return self.player.role() != 'seller'

    def vars_for_template(self):
        return dict(
            role = self.participant.vars['role'],
            pac1 = self.player.buyer_valuation_pac1,
            pac2 = self.player.buyer_valuation_pac2,
            pac3 = self.player.buyer_valuation_pac3,
            pac4 = self.player.buyer_valuation_pac4,
            pac5 = self.player.buyer_valuation_pac5
        )

class buyer_2(Page):
    form_model = 'player'
    form_fields = ['bid_price']

    def vars_for_template(self):
        return dict(
        player = self.player.id_in_group,
        price = self.player.ask_price_fin,
        seller_package = self.player.seller_package
        )

page_sequence = [seller, seller_2, buyer, buyer_2]
