mport itertools
test_dict = {'marketplace': [{'business_status': 'OPERATIONAL', 'geometry': {'location': {'lat': 42.355685, 'lng': -71.0626147}, 'viewport': {'northeast': {'lat': 42.35707367989272, 'lng': -71.06133862010728}, 'southwest': {'lat': 42.35437402010728, 'lng': -71.06403827989273}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png', 'id': '8686575af7b9cbb08a650bf2b51fb3033b95f554', 'name': "Lambert's Marketplace", 'opening_hours': {'open_now': False}, 'photos': [{'height': 3024, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/103646736284519628018">Joseph Pena</a>'], 'photo_reference': 'CmRaAAAA5Hj5VNRrXvOZn29l4CC3ALjVdFt_04E_i_x9am7sM3EM6FyvZTyJqN7ErbxQ5L3oaFuglNWmoSWOgCruhuGzaKMpRjVBDXeNCVFXdFk9o9idgsGtwMePexmJ3cAairA6EhAbW9yMZtxUds-HlHma2v8HGhQMuqYh2Pmieuw0R_9J6n2eqVvHTA', 'width': 4032}], 'place_id': 'ChIJfZmx2Jxw44kR11GqlDbYwfs', 'plus_code': {'compound_code': '9W4P+7X Boston, Massachusetts, United States', 'global_code': '87JC9W4P+7X'}, 'price_level': 1, 'rating': 4.2, 'reference': 'ChIJfZmx2Jxw44kR11GqlDbYwfs', 'scope': 'GOOGLE', 'types': ['florist', 'meal_takeaway', 'restaurant', 'food', 'point_of_interest', 'store', 'establishment'], 'user_ratings_total': 86, 'vicinity': '140 Tremont St, Boston'}]}

def remove_duplicates(dict_raw):
        filtered_dict = {}
        for key in dict_raw:
            # print("key is: ", key, file=)
            filtered_list = []
            for p in dict_raw[key]:
                duplicate = False
                if p in itertools.chain(*filtered_dict.values()):
                        duplicate = True
                        break
                if not duplicate:
                    if 'restaurant' not in p['types'] or p in itertools.chain(*self.food_places.values()):
                        filtered_list.append(p)
            if filtered_list:
                filtered_dict[key] = filtered_list

        dict_raw = filtered_dict

for key in test_dict:
    for p in test_dict[key]:
        print(key, " : before : ", p['name'])

remove_duplicates(test_dict)

for key in test_dict:
            for p in test_dict[key]:
                print(key, " : after : ", p['name'])