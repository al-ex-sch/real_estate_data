##
from src.get_real_estate_data.a_helper.config import cantons_split_apartments, cantons
from src.get_real_estate_data.a_helper.link_generator import LinkGenerator

link_generator = LinkGenerator(cantons, cantons_split_apartments)
links_list = link_generator.get_all_links()
